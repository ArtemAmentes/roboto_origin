import torch
import torch.nn as nn
from .mlp import MLP
from .cnn import CNN

class AttentionEncoder(nn.Module):
    def __init__(self, d_obs:int, embedding_dim=64, h=8, map_size=(17,11), map_resolution=0.1):
        super(AttentionEncoder, self).__init__()

        if embedding_dim <= 3:
            raise ValueError("embedding_dim must exceed the spatial coordinate dimension (3)")
        if embedding_dim % h != 0:
            raise ValueError("embedding_dim must be divisible by the number of attention heads")

        self.embedding_dim = embedding_dim
        self.h = h
        self.L = map_size[0]
        self.W = map_size[1]
        self.map_resolution=map_resolution

        self.register_buffer('pos_encoding', self._create_position_encoding())

        self.cnn = CNN(
            input_dim=(self.W, self.L),
            input_channels=1,
            output_channels=[16, 32, self.embedding_dim - 3],
            kernel_size=3,
            stride=1,
            norm="none",
            padding="replicate",
            activation="elu",
            flatten=False
        )

        self.proprio_linear = MLP(d_obs, self.embedding_dim, [128], "elu")

        # Модуль многоголового внимания
        self.mha = nn.MultiheadAttention(embed_dim=self.embedding_dim, num_heads=self.h, batch_first=True)

        # Нормализация слоя
        self.ln_q = nn.LayerNorm(self.embedding_dim)
        self.ln_kv = nn.LayerNorm(self.embedding_dim)
        self.ln_out = nn.LayerNorm(self.embedding_dim)

    def _create_position_encoding(self):
        x_coords = torch.linspace(0, (self.L - 1) * self.map_resolution, self.L)
        x_center = x_coords.mean()
        x_coords = x_coords - x_center

        y_coords = torch.linspace(0, (self.W - 1) * self.map_resolution, self.W)
        y_center = y_coords.mean()
        y_coords = y_coords - y_center
        
        x_grid, y_grid = torch.meshgrid(x_coords, y_coords, indexing='xy')  # (W, L)
        
        pos_encoding = torch.stack([x_grid, y_grid], dim=0)  #(2, W, L)
        return pos_encoding

    def forward(self, proprioception, map_scans):
        B = map_scans.shape[0]
        map_scans = map_scans.view(B, self.W, self.L, 1)

        # 1. Обработка карты сканирования
        # Извлечение z-значений (высота) и преобразование в формат channels-first (B, 1, W, L)
        z_values = map_scans.permute(0, 3, 1, 2)

        # Обработка z-значений через CNN
        cnn_features = self.cnn(z_values)  # (B, d-3, W, L)

        # Конкатенация с позиционным кодированием и признаками CNN
        pos_encoding_batch = self.pos_encoding.unsqueeze(0).expand(B, -1, -1, -1)
        local_features = torch.cat([pos_encoding_batch, z_values, cnn_features], dim=1)  # (B, d, W, L)

        # Преобразование в точечные признаки (B, L*W, d)
        pointwise_features = local_features.permute(0, 2, 3, 1).contiguous().view(B, self.W * self.L, self.embedding_dim)

        # 2. Обработка проприоцепции
        proprio_embedding = self.proprio_linear(proprioception.unsqueeze(1))  # (B, 1, d)

        # 3. Многоголовое внимание
        # Нормализация
        q = self.ln_q(proprio_embedding)
        kv = self.ln_kv(pointwise_features)

        # Внимание
        attn_output, attn_weights = self.mha(
            query=q, # (B, 1, d)
            key=kv,  # (B, L*W, d)
            value=kv
        )

        map_encoding = self.ln_out(attn_output)

        # reshape to (B, d) & (B, W, L)
        map_encoding = map_encoding.squeeze(1)

        if attn_weights is not None:
            attn_weights = attn_weights.view(B, self.W, self.L)

        return map_encoding, attn_weights


if __name__ == "__main__":
    d = 64  # Размерность MHA
    h = 8  # Количество голов внимания
    d_obs = 78  # Размерность проприоцепции 
    map_size = (17, 11)  # Размер карты
    # Создание модели
    model = AttentionEncoder(d_obs, d, h, map_size, 0.1)

    # Создание примера входных данных
    batch_size = 4
    map_scans = torch.randn(batch_size, map_size[1], map_size[0], 1)  # (4, 11, 17, 1)
    proprioception = torch.randn(batch_size, d_obs)  # (4, 78)

    # Прямой проход
    embedding, attention = model(proprioception, map_scans)

    print(f"Форма входной карты сканирования: {map_scans.shape}")
    print(f"Форма входной проприоцепции: {proprioception.shape}")
    print(f"output embedding shape: {embedding.shape}")
    print(f"output attention shape: {attention.shape}")
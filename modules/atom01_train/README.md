# ATOM01-Train

[![IsaacSim](https://img.shields.io/badge/IsaacSim-5.1.0-silver.svg)](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html)
[![Isaac Lab](https://img.shields.io/badge/IsaacLab-2.3.2-silver)](https://isaac-sim.github.io/IsaacLab)
[![RSL_RL](https://img.shields.io/badge/RSL_RL-3.3.0-silver)](https://github.com/leggedrobotics/rsl_rl)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://docs.python.org/3/whatsnew/3.10.html)
[![Платформа](https://img.shields.io/badge/платформа-linux--64-orange.svg)](https://releases.ubuntu.com/22.04/)
[![Платформа](https://img.shields.io/badge/платформа-windows--64-orange.svg)](https://www.microsoft.com/en-us/)
[![Лицензия](https://img.shields.io/badge/лицензия-BSD--3-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

## Обзор

Репозиторий для обучения шагающего робота на базе IsaacLab. Прозрачный workflow, низкая сложность рефакторинга окружения, модульная архитектура.

**Мейнтейнер**: Zhihao Liu  
**Контакт**: ZhihaoLiu_hit@163.com

**Ключевые особенности:**

- `Простота реорганизации` — прямой workflow, детальная настройка логики окружения
- `Изоляция` — работа вне ядра Isaac Lab, изменения не затрагивают core-репо
- `Долгосрочная поддержка` — синхронизация с обновлениями Isaac Sim и Isaac Lab

## Установка

ATOM01-Train рассчитан на актуальные версии Isaac Sim / Isaac Lab.

1. Установите Isaac Lab по [официальной инструкции](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html). Рекомендуется установка через conda.

2. Клонируйте репозиторий отдельно от Isaac Lab:

```bash
git clone https://github.com/Roboparty/atom01_train.git
```

3. Установите библиотеки (в окружении с Isaac Lab):

```bash
cd atom01_train
git submodule update --init --recursive
cd robolab
pip install -e .
cd ..
cd rsl_rl
pip install -e .
cd ..
```

4. Проверка:

```bash
python robolab/scripts/tools/list_envs.py
```

## Использование

### Обучение

```bash
python robolab/scripts/rsl_rl/train.py --task=<ENV_NAME> --headless --logger=tensorboard --num_envs=8192
```

### Воспроизведение

```bash
python robolab/scripts/rsl_rl/play.py --task=<ENV_NAME> --num_envs=1
```

### Sim2Sim

```bash
python robolab/scripts/mujoco/sim2sim_atom01.py --load_model "{путь к экспортированной policy.pt}"
```

### Подготовка данных движения

Данные для AMP и BeyondMimic: [GMR](https://github.com/Roboparty/GMR).

Порядок сочленений в датасете должен соответствовать URDF/XML. Используйте `.yaml` с маппингом (пример: `scripts/tools/retarget/config/atom01.yaml`) и переупорядочивайте через `scripts/tools/retarget/dataset_retarget.py`.

## Благодарности

- [IsaacLab](https://github.com/isaac-sim/IsaacLab)
- [rsl_rl](https://github.com/leggedrobotics/rsl_rl)
- [legged_gym](https://github.com/leggedrobotics/legged_gym)
- [legged_lab](https://github.com/zitongbai/legged_lab)
- [robot_lab](https://github.com/fan-ziqi/robot_lab)

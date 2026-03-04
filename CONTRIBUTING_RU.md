# Как внести вклад в ROBOTO_ORIGIN

Спасибо за интерес к проекту ROBOTO_ORIGIN! В этом документе — рекомендации по контрибьютингу.

## Важно: структура репозитория

**Репозиторий `roboto_origin` — только снимок (snapshot).**

Он служит ежедневно обновляемой агрегацией всех sub-репозиториев и даёт готовую к работе кодовую базу без инициализации submodules.

### Что это значит

- **НЕ** создавайте pull request и issues в `roboto_origin`
- **Направляйте** contributions в соответствующий sub-репозиторий
- Основной репозиторий обновляется из sub-репо автоматически

## Как внести вклад

### 1. Выберите нужный sub-репозиторий

| Sub-репозиторий | Назначение |
|-----------------|------------|
| [Atom01_hardware](https://github.com/Roboparty/Atom01_hardware) | Механика, CAD, PCB, BOM |
| [atom01_deploy](https://github.com/Roboparty/atom01_deploy) | ROS2, драйверы, IMU, моторы |
| [atom01_train](https://github.com/Roboparty/atom01_train) | RL, Isaac Lab, симуляция |
| [atom01_description](https://github.com/Roboparty/atom01_description) | URDF, меши, кинематика |

### 2. Форк и клон

```bash
git clone https://github.com/YOUR_USERNAME/<sub-repo>.git
cd <sub-repo>
git remote add upstream https://github.com/Roboparty/<sub-repo>.git
```

### 3. Создайте ветку

```bash
git checkout -b feature/название-фичи
```

### 4. Внесите изменения и оформите Pull Request

Следуйте стилю кода, обновляйте документацию, пишите понятные коммиты.

### 5. Лицензия

Все вклады распространяются под GPLv3.

## Контакты

- **QQ Group:** 1078670917
- **Email:** zhangbaoxin@roboparty.com
- **GitHub Issues:** в соответствующем sub-репозитории

**Помните:** вклад вносят в sub-репозитории, а не в основной snapshot.

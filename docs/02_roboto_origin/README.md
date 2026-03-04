# roboto_origin

Форк проекта [Roboparty/roboto_origin](https://github.com/Roboparty/roboto_origin) с полной русской документацией.

---

## О проекте

**roboto_origin** — полностью опенсорсный DIY-гуманоидный робот (GPL v3). ROS2, Isaac Lab, Python, C++. Сборка через Taobao/Цзяличуан. Прототип разработан за 4 месяца командой RoboParty (Китай).

## Модули

| Модуль | Описание | Репозиторий |
|--------|----------|-------------|
| Atom01_hardware | Конструкция, CAD, PCB, BOM | [Atom01_hardware](https://github.com/Roboparty/Atom01_hardware) |
| atom01_deploy | ROS2-драйверы, middleware, IMU, моторы | [atom01_deploy](https://github.com/Roboparty/atom01_deploy) |
| atom01_train | RL-алгоритмы, Isaac Lab, Sim2Sim | [atom01_train](https://github.com/Roboparty/atom01_train) |
| atom01_description | URDF, кинематика, динамика | [atom01_description](https://github.com/Roboparty/atom01_description) |

---

## Содержание раздела

- [**Архитектура репозитория**](АРХИТЕКТУРА_РЕПОЗИТОРИЯ_ROBOTO_ORIGIN.md) — схема, структура, дерево файлов, карта перевода, стратегия 100% русификации
- [**README модулей (русский)**](README_модулей_RU.md) — описание Atom01_hardware, atom01_deploy, atom01_train, atom01_description
- [**Перевод репозитория на русский**](ПЕРЕВОД_РЕПОЗИТОРИЯ_НА_РУССКИЙ.md) — описание цели и объёма: все файлы и комментарии в коде на русском
- [Интеграция с OpenClaw](интеграция_openclaw.md) — связка roboto_origin + AI-агенты
- [русская_документация/](русская_документация/) — черновики русских переводов README, CONTRIBUTING и др.

## Work packages по форку

- WP-R1: Форк/клонирование roboto_origin и sub-репозиториев
- WP-R2: Перевод README.md → README_RU.md
- WP-R3: Перевод CONTRIBUTING.md, CODE_OF_CONDUCT.md
- WP-R4: Перевод Humanoid Robot Know-How Documentation
- WP-R5: Перевод README в каждом sub-репозитории
- WP-R6 (опц.): Docstrings и комментарии в коде на русском

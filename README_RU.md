# ROBOTO_ORIGIN — полностью опенсорсный DIY-гуманоидный робот

[![Лицензия: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![ROS2](https://img.shields.io/badge/ROS2-Humble-silver)](https://docs.ros.org/en/humble/index.html) [![Isaac Sim](https://img.shields.io/badge/IsaacSim-4.5.0-silver.svg)](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html) [![Isaac Lab](https://img.shields.io/badge/IsaacLab-2.1.1-silver)](https://isaac-sim.github.io/IsaacLab)

---

![Обзор робота](assets/1280X1280.JPEG)

**English:** [README.md](README.md) | **中文:** [README_cn.md](README_cn.md)

## Проект «Национальная платформа российской робототехники»

Русскоязычная документация, исследование рынка, OpenClaw, презентация для Москвы: **[docs/](docs/)**

---

## О проекте

Мы — **RoboParty**, основаны 21 февраля 2025 года. Разработку гуманоидных роботов начали в апреле и за четыре месяца завершили прототип **ROBOTO_ORIGIN**. Мы всегда придерживались философии открытого кода. Весь R&D-процесс ROBOTO_ORIGIN — структуры, электроника, обучение и развёртывание — открыт.

По мере развития новых роботов мы понимаем, что высокопроизводительного робота нельзя создать только своими силами. Поэтому мы решили официально открыть этот бегающий и прыгающий прототип, чтобы зафиксировать наш путь.

> Этот робот можно полностью собрать, закупив компоненты на Taobao и изготовив детали через Цзяличуан. С нашим открытым кодом для обучения и развёртывания вы легко сможете добиться ходьбы и бега.

В будущем мы постепенно добавим в репозиторий алгоритмы управления движением, реализованные на этом роботе. Но как полностью открытый робот, его функциональность определяется множеством разработчиков и пользователей, поэтому скоро будет запущена творческая мастерская.

---

## Документация

**[Humanoid Robot Know-How Documentation](https://roboparty.com/roboto_origin/doc)** — полная R&D-документация прототипа

### Как внести вклад

**Важно:** Репозиторий `roboto_origin` — агрегатор снимков. Сообщения об ошибках и код направляйте в соответствующие sub-репозитории.

| Sub-репозиторий | Направления контрибьюта |
|-----------------|-------------------------|
| **[Atom01_hardware](https://github.com/Roboparty/Atom01_hardware)** | Механика, CAD, PCB, BOM |
| **[atom01_deploy](https://github.com/Roboparty/atom01_deploy)** | ROS2-драйверы, middleware, IMU, моторы |
| **[atom01_train](https://github.com/Roboparty/atom01_train)** | RL-алгоритмы, Isaac Lab, Sim2Sim |
| **[atom01_description](https://github.com/Roboparty/atom01_description)** | URDF, кинематика, динамика |

**Подробнее:** [CONTRIBUTING.md](CONTRIBUTING.md)

**BOM:** [assets/BOM_EN.md](./assets/BOM_EN.md)

---

## Quick Start

```bash
git clone https://github.com/Roboparty/roboto_origin.git
cd roboto_origin
git pull
```

Перейдите в каталоги `modules/...` и следуйте README в каждом модуле.

---

## Кодекс поведения

Проект руководствуется [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Отказ от ответственности

Программное обеспечение предоставляется «как есть», без гарантий. Команды, генерируемые софтом, выполняются на физическом железе — ответственность за действия робота несёт оператор. **RoboParty не несёт ответственности** за использование, модификацию или распространение.

**Проект распространяется под лицензией GNU GPL v3. См. [LICENSE](LICENSE).**

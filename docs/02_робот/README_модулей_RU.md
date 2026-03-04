# Модули робот — краткое описание на русском

Русскоязычное описание модулей проекта Atom01. Оригиналы: [Atom01_hardware](https://github.com/Roboparty/Atom01_hardware), [atom01_deploy](https://github.com/Roboparty/atom01_deploy), [atom01_train](https://github.com/Roboparty/atom01_train), [atom01_description](https://github.com/Roboparty/atom01_description).

---

## Atom01_hardware

Центральный репозиторий аппаратной части робота ROBOTO. Цель — снизить барьер входа за счёт полного open-source стека: от механики до электроники.

### Модули

| Модуль | Описание | Документация |
|--------|----------|--------------|
| **Корпус робота** (механика) | Конструкция и сборка | [atom01_mechnaic/README.md](https://github.com/Roboparty/Atom01_hardware/tree/main/atom01_mechnaic) |
| **Плата питания** | Распределение питания 48V, разъёмы XT30/XT60 | [Roboto_Power/README.md](https://github.com/Roboparty/Atom01_hardware/tree/main/atom01_pcb/Roboto_Power) |
| **Модуль связи USB-CAN** | USB → 4 канала CAN, Linux, терминация 120Ω | [Roboto_Usb2Can/README.md](https://github.com/Roboparty/Atom01_hardware/tree/main/atom01_pcb/Roboto_Usb2Can) |

### Порядок сборки

1. **Подготовка:** скачать BOM, закупить компоненты, заказать печатные платы
2. **Механика:** следовать Assembly_Guide в папке корпуса
3. **Электроника:** изготовить плату питания и USB-CAN, прошить прошивку
4. **Подключение:** батарея → плата питания, USB-CAN → хост-компьютер (проверить полярность)

---

## atom01_deploy

Фреймворк развёртывания на базе ROS2 с модульной архитектурой.

### Поддерживаемые платформы

- **Orange Pi 5 Plus** — Ubuntu 22.04, ядро 5.10, real-time
- **RDK X5** — Ubuntu 22.04, ядро 6.1.83

### Подключение оборудования

- **can0** — левая нога
- **can1** — правая нога и талия
- **can2** — левая рука
- **can3** — правая рука

Порядок USB-CAN при вставке определяет нумерацию. Рекомендуется USB 3.0. IMU и геймпад — USB 2.0.

### Запуск

```bash
./tools/start_robot.sh
```

### Управление геймпадом

- **A** — инициализация/деинициализация моторов
- **X** — сброс моторов
- **B** — старт/пауза inference
- **Y** — переключение геймпад / cmd_vel
- **LB** — смена режима политики

### ROS2-сервисы

```bash
ros2 service call /init_motors std_srvs/srv/Trigger
ros2 service call /start_inference std_srvs/srv/Trigger
ros2 service call /stop_inference std_srvs/srv/Trigger
# и др.
```

---

## atom01_train

Обучение с подкреплением в Isaac Lab, перенос Sim2Sim в MuJoCo.

### Подмодули

- **robolab** — окружение Isaac Lab
- **rsl_rl** — алгоритмы RL

Требует: Isaac Sim 4.5.0, Isaac Lab 2.1.1.

---

## atom01_description

URDF-модели, MJCF для MuJoCo, меши, ассеты местности.

Используется в atom01_train (симуляция) и atom01_deploy (визуализация).

---

## См. также

- [Сборка робота](сборка_робота.md)
- [Архитектура репозитория](АРХИТЕКТУРА_РЕПОЗИТОРИЯ_РОБОТ.md)
- [BOM на русском](../../assets/BOM_RU.md)

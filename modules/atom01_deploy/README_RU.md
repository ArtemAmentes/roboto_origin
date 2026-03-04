# ATOM01 ROS2 Deploy

[![ROS2](https://img.shields.io/badge/ROS2-Humble-silver)](https://docs.ros.org/en/humble/index.html)
![C++](https://img.shields.io/badge/C++-17-blue)
[![Linux platform](https://img.shields.io/badge/platform-linux--x86_64-orange.svg)](https://releases.ubuntu.com/22.04/)
[![Linux platform](https://img.shields.io/badge/platform-linux--aarch64-orange.svg)](https://releases.ubuntu.com/22.04/)

[English](README.md) | [中文](README_CN.md) | [Русский](README_RU.md)

## Обзор

Этот репозиторий предоставляет фреймворк развёртывания на базе ROS2 как middleware с модульной архитектурой для лёгкой кастомизации и расширения.

**Мейнтейнер**: Zhihao Liu  
**Контакт**: <ZhihaoLiu_hit@163.com>

**Ключевые особенности:**

- `Простота использования` — полный подробный код для обучения и модификации.
- `Изоляция` — разные функции реализованы в разных пакетах, поддерживаются пользовательские пакеты.
- `Долгосрочная поддержка` — репозиторий обновляется вместе с кодом обучения.

## Настройка окружения

Код развёртывания запускается на Orange Pi 5 Plus с Ubuntu 22.04 и ядром 5.10. Конфигурация выполняется под Orange Pi 5 Plus.

Также поддерживается развёртывание на RDK X5 (Ubuntu 22.04, ядро 6.1.83). Детали — в разделе про Orange Pi 5 Plus, отличия указаны отдельно.

Сначала установите ROS2 Humble по [официальной инструкции](https://docs.ros.org/en/humble/Installation.html).

Зависимости: ccache, fmt, spdlog, eigen3:

```bash
sudo apt update && sudo apt install -y ccache libfmt-dev libspdlog-dev libeigen3-dev
```

Установите RT-ядро 5.10 для Orange Pi 5 Plus:

```bash
git clone https://github.com/Roboparty/atom01_deploy.git
cd atom01_deploy
git submodule update --init --recursive
cd assets
sudo apt install ./*.deb
cd ..
```

> **Примечание**: Для RDK X5 этот шаг не требуется — прошейте образ с предустановленным RT-ядром.

Настройте права на real-time приоритеты:

```bash
sudo nano /etc/security/limits.conf
```

Добавьте в конец (замените `orangepi` на имя пользователя):

```bash
orangepi   -   rtprio   98
orangepi   -   memlock  unlimited
```

> Для RDK X5 пользователь по умолчанию — `sunrise`.

Перезагрузите устройство и проверьте:

```bash
ulimit -r
```

Вывод **98** означает успешную настройку.

## Подключение оборудования

В драйвере моторов: can0 — левая нога, can1 — правая нога и пояс, can2 — левая рука, can3 — правая рука. По умолчанию нумерация по порядку вставки USB-to-CAN (первый — can0). Рекомендуется подключать USB-to-CAN в порт USB 3.0. IMU и геймпад — в USB 2.0.

Настройте udev-правила для привязки портов к устройствам (пример в `99-auto-up-devs.rules`). Мониторинг USB:

```bash
sudo udevadm monitor
```

При вставке устройства отобразится KERNELS (например `3-8`). После правок:

```bash
sudo cp 99-auto-up-devs.rules /etc/udev/rules.d/
sudo udevadm control --reload
sudo udevadm trigger
```

Для RDK X5 используйте `99-auto-up-devs-sunrise.rules`.

## Использование

### Запуск робота

```bash
./tools/start_robot.sh
```

### Управление с геймпада

- **A**: Инициализация/деинициализация моторов
- **X**: Сброс моторов
- **B**: Старт/пауза inference
- **Y**: Переключение Gamepad / cmd_vel
- **LB**: Смена режима политики (режимы beyondmimic / interrupt)

### Сервисный интерфейс

```bash
ros2 service call /init_motors std_srvs/srv/Trigger
ros2 service call /deinit_motors std_srvs/srv/Trigger
ros2 service call /start_inference std_srvs/srv/Trigger
ros2 service call /stop_inference std_srvs/srv/Trigger
ros2 service call /clear_errors std_srvs/srv/Trigger
ros2 service call /set_zeros std_srvs/srv/Trigger
ros2 service call /reset_joints std_srvs/srv/Trigger
ros2 service call /refresh_joints std_srvs/srv/Trigger
```

## Python SDK

Перед использованием: `source install/setup.bash`.

### 1. IMU SDK (`imu_py`)

- `create_imu(...)` → IMUDriver
- `get_quat()`, `get_ang_vel()`, `get_lin_acc()`, `get_temperature()`

### 2. Motor SDK (`motors_py`)

Режимы: `NONE`, `MIT`, `POS`, `SPD`.  
Методы: `create_motor()`, `init_motor()`, `motor_mit_cmd()`, `motor_pos_cmd()`, `get_motor_pos()`, и др.

### 3. Robot SDK (`robot_py`)

Класс `RobotInterface` — единый интерфейс управления роботом.

```python
import robot_py
robot = robot_py.RobotInterface("config/robot.yaml")
robot.init_motors()
robot.apply_action([0.0] * 23)
```

Подробнее — в папке `scripts/`.

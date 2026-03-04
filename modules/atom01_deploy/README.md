# ATOM01 ROS2 Deploy

[![ROS2](https://img.shields.io/badge/ROS2-Humble-silver)](https://docs.ros.org/en/humble/index.html)
![C++](https://img.shields.io/badge/C++-17-blue)
[![Платформа](https://img.shields.io/badge/платформа-linux--x86_64-orange.svg)](https://releases.ubuntu.com/22.04/)
[![Платформа](https://img.shields.io/badge/платформа-linux--aarch64-orange.svg)](https://releases.ubuntu.com/22.04/)

## Обзор

Фреймворк развёртывания на базе ROS2 с модульной архитектурой для лёгкой кастомизации и расширения.

**Мейнтейнер**: Zhihao Liu  
**Контакт**: <ZhihaoLiu_hit@163.com>

**Ключевые особенности:**

- `Простота использования` — полный подробный код для обучения и модификации
- `Изоляция` — разные функции реализованы в разных пакетах
- `Долгосрочная поддержка` — репозиторий обновляется вместе с кодом обучения

## Настройка окружения

Код развёртывания запускается на Orange Pi 5 Plus с Ubuntu 22.04 и ядром 5.10.

Также поддерживается RDK X5 (Ubuntu 22.04, ядро 6.1.83).

Сначала установите ROS2 Humble по [официальной инструкции](https://docs.ros.org/en/humble/Installation.html).

Установите зависимости:

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

> **Примечание**: Для RDK X5 прошейте образ с предустановленным RT-ядром.

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

Перезагрузите и проверьте:

```bash
ulimit -r
```

Вывод **98** означает успех.

## Подключение оборудования

В драйвере моторов: can0 — левая нога, can1 — правая нога и пояс, can2 — левая рука, can3 — правая рука. Нумерация по порядку вставки USB-to-CAN.

Настройте udev-правила для привязки портов (пример в `99-auto-up-devs.rules`).

Мониторинг USB:

```bash
sudo udevadm monitor
```

После настройки:

```bash
sudo cp 99-auto-up-devs.rules /etc/udev/rules.d/
sudo udevadm control --reload
sudo udevadm trigger
```

## Использование

### Запуск робота

```bash
./tools/start_robot.sh
```

### Управление с геймпада

| Кнопка | Действие |
|--------|----------|
| **A** | Инициализация/деинициализация моторов |
| **X** | Сброс моторов |
| **B** | Старт/пауза inference |
| **Y** | Переключение Gamepad / cmd_vel |
| **LB** | Смена режима политики |

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

```python
import imu_py
imu = imu_py.IMUDriver.create_imu(8, "serial", "/dev/ttyUSB0", "HIPNUC", 921600)
quat = imu.get_quat()
```

Методы: `get_imu_id()`, `get_ang_vel()`, `get_quat()`, `get_lin_acc()`, `get_temperature()`

### 2. Motor SDK (`motors_py`)

Режимы: `NONE`, `MIT`, `POS`, `SPD`

```python
import motors_py
motor = motors_py.MotorDriver.create_motor(1, "can", "can0", "DM", 0, 16)
motor.init_motor()
motor.set_motor_control_mode(motors_py.MotorControlMode.MIT)
motor.motor_mit_cmd(0.0, 0.0, 5.0, 1.0, 0.0)
```

### 3. Robot SDK (`robot_py`)

```python
import robot_py
robot = robot_py.RobotInterface("config/robot.yaml")
robot.init_motors()
robot.apply_action([0.0] * 23)
```

Методы: `init_motors()`, `deinit_motors()`, `reset_joints()`, `apply_action()`, `get_joint_q()`, `get_joint_vel()`, `get_quat()`, `get_ang_vel()`

Подробнее — в папке `scripts/`.

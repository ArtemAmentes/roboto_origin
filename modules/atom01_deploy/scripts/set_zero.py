#!/usr/bin/env python3
"""Инструмент калибровки нулевой точки моторов."""
import os
import sys
import yaml
import motors_py
import time


def load_config(config_path: str) -> dict:
    """Загрузка конфигурации из YAML-файла."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def create_motors(config: dict) -> list:
    """Создание объектов моторов по конфигурации."""
    motors = []
    motor_ids = config['motor_id']
    motor_interface_type = config['motor_interface_type']
    motor_interfaces = config['motor_interface']
    motor_num = config['motor_num']
    motor_type = config['motor_type']
    motor_models = config['motor_model']
    master_id_offset = config['master_id_offset']
    motor_zero_offsets = config['motor_zero_offset']
    
    motor_idx = 0
    for interface_idx, num in enumerate(motor_num):
        interface = motor_interfaces[interface_idx]
        for _ in range(num):
            if motor_idx >= len(motor_ids):
                break
            motor_id = motor_ids[motor_idx]
            motor_model = motor_models[motor_idx] if motor_idx < len(motor_models) else 0
            motor_zero_offset = motor_zero_offsets[motor_idx] if motor_idx < len(motor_zero_offsets) else 0.0
            
            motor = motors_py.MotorDriver.create_motor(
                motor_id=motor_id,
                interface_type=motor_interface_type,
                interface=interface,
                motor_type=motor_type,
                motor_model=motor_model,
                master_id_offset=master_id_offset,
                motor_zero_offset=motor_zero_offset,
            )
            motors.append({
                'motor': motor,
                'motor_id': motor_id,
                'interface': interface,
                'index': motor_idx
            })
            motor_idx += 1
    
    return motors


def set_damping_mode(motor):
    """Установка режима демпфирования."""
    motor.set_motor_control_mode(motors_py.MotorControlMode.MIT)
    motor.motor_mit_cmd(0.0, 0.0, 0.0, 2.0, 0.0)


def calibrate_motor(motor_info: dict):
    """Калибровка одного мотора."""
    motor = motor_info['motor']
    motor_id = motor_info['motor_id']
    interface = motor_info['interface']
    
    print(f"\n{'='*50}")
    print(f"Калибровка мотора ID: {motor_id} (интерфейс: {interface})")
    print(f"{'='*50}")
    
    print("Включение мотора...")
    motor.init_motor()
    time.sleep(0.3)
    
    print("Установка режима демпфирования (MIT: 0, 0, 0, 2, 0)...")
    set_damping_mode(motor)
    time.sleep(0.1)
    
    print("\n>>> Вручную установите мотор в нулевую позицию <<<")
    print("Подсказка: мотор в режиме демпфирования, можно свободно вращать")
    
    try:
        while True:
            motor.motor_mit_cmd(0.0, 0.0, 0.0, 2.0, 0.0)
            
            pos = motor.get_motor_pos()
            print(f"\rТекущая позиция: {pos:+.6f} рад | Нажмите Enter для подтверждения...", end='', flush=True)
            
            import select
            if select.select([sys.stdin], [], [], 0.05)[0]:
                sys.stdin.readline()
                break
            
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("\n\nКалибровка прервана пользователем")
        motor.deinit_motor()
        raise
    
    motor.set_motor_zero()
    print(f"\n\nМотор {motor_id} откалиброван!")
    
    print("Отключение мотора...")
    motor.deinit_motor()
    time.sleep(0.2)


def main():
    """Основная функция калибровки."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config', 'set_zero.yaml')
    
    print("="*60)
    print("        Инструмент калибровки нулевой точки моторов")
    print("="*60)
    print(f"\nФайл конфигурации: {config_path}\n")
    
    try:
        config = load_config(config_path)
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        return 1
    
    print("Информация о конфигурации:")
    print(f"  - ID моторов: {config['motor_id']}")
    print(f"  - Тип моторов: {config['motor_type']}")
    print(f"  - Тип интерфейса: {config['motor_interface_type']}")
    print(f"  - Интерфейсы: {config['motor_interface']}")
    print(f"  - Модели моторов: {config['motor_model']}")
    print("\n" + "-"*60)
    input("Нажмите Enter для начала калибровки...")
    print("-"*60)
    
    try:
        motors = create_motors(config)
        print(f"\nСоздано {len(motors)} объектов моторов")
    except Exception as e:
        print(f"Ошибка создания моторов: {e}")
        return 1
    
    try:
        for motor_info in motors:
            calibrate_motor(motor_info)
            print(f"Мотор {motor_info['motor_id']} откалиброван!")
    except KeyboardInterrupt:
        print("\n\nКалибровка прервана пользователем")
        return 1
    except Exception as e:
        print(f"\nОшибка калибровки: {e}")
        return 1
    
    print("\n" + "="*60)
    print("        Калибровка всех моторов завершена!")
    print("="*60)
    
    print("\nПроцесс калибровки завершён")
    return 0


if __name__ == '__main__':
    sys.exit(main())

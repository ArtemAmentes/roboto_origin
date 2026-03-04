#!/usr/bin/env python3
"""Пример работы с моторами через CAN-шину."""
import motors_py
import time

def example_can_motor():
    """Пример использования мотора, подключённого через CAN."""
    print("=== Пример работы с CAN-мотором ===")
    motors = []
    try:
        for i in range(1, 2):
            motors.append(motors_py.MotorDriver.create_motor(
            motor_id=i,
            interface_type="can",
            interface="can0",
            motor_type="DM",
            motor_model=0,
            master_id_offset=16,
        ))
        print("Мотор успешно создан!")
    except Exception as e:
        print(f"Ошибка создания мотора: {e}")
        return
    
    try:
        print("Включение мотора...")
        for motor in motors:
            motor.init_motor()
        
        print("\n=== Пример управления в режиме MIT ===")
        motors[0].set_motor_control_mode(motors_py.MotorControlMode.MIT)
        
        target_pos = -0.5
        target_vel = 0.0
        kp = 5.0
        kd = 1.0
        torque = 0.0
        
        motors[0].motor_mit_cmd(target_pos, target_vel, kp, kd, torque)
            
        # Чтение состояния мотора
        pos = motors[0].get_motor_pos()
        vel = motors[0].get_motor_spd()
        current = motors[0].get_motor_current()
        temp = motors[0].get_motor_temperature()
        error_id = motors[0].get_error_id()
        
        print(f"Позиция: {pos:.4f} рад, Скорость: {vel:.4f} рад/с, "
              f"Ток: {current:.4f} А, Температура: {temp:.2f}°C, Код ошибки: {error_id}")
        time.sleep(1)
    except Exception as e:
        print(f"Ошибка при управлении мотором: {e}")
    finally:
        for motor in motors:
            print("Отключение мотора...")
            motor.deinit_motor()


if __name__ == "__main__":
    example_can_motor()

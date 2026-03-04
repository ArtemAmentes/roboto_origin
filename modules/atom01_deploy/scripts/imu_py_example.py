#!/usr/bin/env python3
"""Пример работы с IMU через последовательный порт."""
import imu_py
import time

def example_serial_imu():
    """Пример использования IMU, подключённого через serial."""
    print("=== Пример работы с IMU (serial) ===")
    try:
        imu = imu_py.IMUDriver.create_imu(
            imu_id=8,
            interface_type="serial",
            interface="/dev/ttyUSB0",
            imu_type="HIPNUC",
            baudrate=921600
        )
    except Exception as e:
        print(f"Ошибка создания IMU: {e}")
        return
    
    print(f"ID IMU: {imu.get_imu_id()}")
    
    for i in range(1000):
        quat = imu.get_quat()
        print(f"Кватернион: w={quat[0]:.4f}, x={quat[1]:.4f}, y={quat[2]:.4f}, z={quat[3]:.4f}")
        
        ang_vel = imu.get_ang_vel()
        print(f"Угловая скорость: x={ang_vel[0]:.4f}, y={ang_vel[1]:.4f}, z={ang_vel[2]:.4f} рад/с")
        
        lin_acc = imu.get_lin_acc()
        print(f"Линейное ускорение: x={lin_acc[0]:.4f}, y={lin_acc[1]:.4f}, z={lin_acc[2]:.4f} м/с²")
        
        temp = imu.get_temperature()
        print(f"Температура: {temp:.2f}°C")
        
        print("-" * 50)
        time.sleep(0.01)

if __name__ == "__main__":
    example_serial_imu()

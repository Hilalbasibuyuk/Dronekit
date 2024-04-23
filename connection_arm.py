from dronekit import connect, VehicleMode
import time

baglanilan_port = "127.0.0.1:14550"
drone = connect(baglanilan_port,wait_ready = True, baud = 57600, timeout = 200)
print("Bağlantı başarılı!")

while not drone.is_armable:
    print("Arm edilmek için hazır")
    time.sleep(1)


drone.mode = VehicleMode("GUIDED") # GUIDED moduna alındıktan sonra arm edilme işlemi başlatılmalı
print("Drone guided moduna alındı")

print("Motorlar arm ediliyor")
drone.armed = True
print("Motorlar arm edildi")

while not drone.armed:
    print("Arm edilmeyi bekliyor")
    time.sleep(1)

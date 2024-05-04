from dronekit import Command, connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

plane = connect("127.0.0.1:14550", wait_ready = True)

while plane.is_armable is not True:
    print("Uçak arm edilebilir durumda değil")
    time.sleep(1)

print("Uçak arm edilebilir")
plane.mode= VehicleMode("GUIDED")

plane.armed = True

while plane.armed is not True:
    print("Uçak arm ediliyor")
    time.sleep(1)

plane.mode = VehicleMode("TAKEOFF")
plane.simple_takeoff(10)

while plane.location.global_relative_frame.alt < 10 * 0.9:
    print("İha hedefe yükseliyor.")
    time.sleep(1)

def gorev_ekle():
    global komut
    komut = plane.commands

    komut.clear()
    time.sleep(1)

    
    #TAKEOFF
    komut.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink. MAV_CMD_NAV_TAKEOFF,0,0,0,0,0,0,0,0,10))

    # WAYPOINT
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 40.26653517 ,  -111.63593936 , 20))
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 40.26802872,  -111.63749938, 30))

    #RTL
    
    komut.add(Command(0,0,0,3,21,0,0,0,0,0,15,plane.home_location.lat,plane.home_location.lon,0))
   
    #DOĞRULAMA
    komut.add(Command(0,0,0,3,21,0,0,0,0,0,0,plane.home_location.lat,plane.home_location.lon,0))

    komut.upload()
    print("Komutlar yükleniyor...")

gorev_ekle()

komut.next=0
plane.mode = VehicleMode("AUTO")
print("Uçak auto moduna alındı.")

while True:
    next_waypoint = komut.next
    print(f"Sıradaki komut {next_waypoint}")
    time.sleep(1)

    if next_waypoint == 4:
        print("Görev bitti")
        break

print("Döngüden çıkıldı")

from dronekit import connect, VehicleMode
import time
connection_string="127.0.0.1:14550"

plane=connect(connection_string,wait_ready=True,timeout=100)

def arm_ol_ve_yuksel(hedef_yukseklik):
    while plane.is_armable==False:
        print("Arm için gerekli şartlar sağlanamadı.")
        time.sleep(1)
        print("Uçak şu anda arm edilebilir")

        plane.mode=VehicleMode("TAKEOFF") # Plane kalkışı için takeoff moduna alırız
        while plane.mode=='TAKEOFF':
            print('TAKEOFF moduna geçiş yapiliyor')
            time.sleep(1.5)

        print("TAKEOFF moduna geçiş yapıldı")
        plane.armed=True
        while plane.armed is False:
            print("Arm için bekleniliyor")
            time.sleep(1)

        print("Uçak arm olmustur")
        
        plane.simple_takeoff(hedef_yukseklik)
        while plane.location.global_relative_frame.alt<=hedef_yukseklik*0.94:
            print("Şu anki yükseklik{}".format(plane.location.global_relative_frame.alt))
            time.sleep(0.5)
        print("Takeoff gerçekleşti")


arm_ol_ve_yuksel(60)

while True:
    if not plane.is_armable or not plane.system_status.ok:
        print("Fail-safe moduna alındı. Uçak arm edilemez ve durumu uygun değil")
        break
    if not plane.last_heartbeat:
        print("Fail-safe moduna alındı.Bağlantı kaybı var")
        break
    if plane.battery==15:
        print("Fail-safe moduna alındı. Düşük batarya")

    if plane.mode.name != "RTL":
        plane.mode = VehicleMode("RTL")
        while not plane.mode.name == "RTL":
            print("Fail-safe moduna geçiş yapılıyor...")
            time.sleep(1)
            if plane.mode == VehicleMode("Fail-safe"):
                break
        print("Uçak Fail-safe moduna alındı")

    time.sleep(1)

from dronekit import connect, VehicleMode
import time
connection_string="127.0.0.1:14550"

plane=connect(connection_string,wait_ready=True,timeout=100)

def arm_ol_ve_yuksel(hedef_yukseklik):
    while plane.is_armable==False:
        print("Arm içi gerekli şartlar sağlanamadı.")
        time.sleep(1)
        print("Uçak su anda armedilebilir")

        plane.mode=VehicleMode("TAKEOFF") # Plane kalkışı için takeoff moduna alırız
        while plane.mode=='TAKEOFF':
            print('TAKEOFF moduna geçiş yapılıyor')
            time.sleep(1.5)

        print("TAKEOFF moduna geçiş yapıldı")
        plane.armed=True
        while plane.armed is False:
            print("Arm için bekleniliyor")
            time.sleep(1)

        print("Uçak arm olmuştur")
        
        plane.simple_takeoff(hedef_yukseklik)
        while plane.location.global_relative_frame.alt<=hedef_yukseklik*0.94:
            print("Şu anki yükseklik{}".format(plane.location.global_relative_frame.alt))
            time.sleep(0.5)
        print("Takeoff gerçekleşti")


arm_ol_ve_yuksel(25)

if plane.mode.name != "STABILIZE": # In stabilize mode the throttle is limited by the THR_MIN and THR_MAX settings.
    plane.mode = VehicleMode("STABILIZE")
    while not plane.mode.name == "STABILIZE":
        print("Uçak STABILIZE moduna alınıyor...")
        time.sleep(1)
        if plane.mode == VehicleMode("STABILIZE"):
            break
    print("Uçak STABILIZE moduna alındı")

if plane.mode.name != "LOITER": # Draw a circle in air
    plane.mode = VehicleMode("LOITER")
    while not plane.mode.name == "LOITER":
        print("Uçak LOITER moduna alınıyor...")
        time.sleep(1)
        if plane.mode == VehicleMode("LOITER"):
            break
    print("Uçak LOITER moduna alındı")
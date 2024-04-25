from dronekit import connect, VehicleMode
import time
connection_string="127.0.0.1:14550"

plane=connect(connection_string,wait_ready=True,timeout=100)

def arm_ol_ve_yuksel(hedef_yukseklik):
	while plane.is_armable==False:
		print("Arm ici gerekli sartlar saglanamadi.")
		time.sleep(1)
	print("Iha su anda armedilebilir")

	plane.mode=VehicleMode("TAKEOFF") # Plane kalkışı için takeoff moduna alırız
	while plane.mode=='TAKEOFF':
		print('TAKEOFF moduna gecis yapiliyor')
		time.sleep(1.5)

	print("TAKEOFF moduna gecis yapildi")
	plane.armed=True
	while plane.armed is False:
		print("Arm icin bekleniliyor")
		time.sleep(1)

	print("Ihamiz arm olmustur")
	
	plane.simple_takeoff(hedef_yukseklik)
	while plane.location.global_relative_frame.alt<=hedef_yukseklik*0.94:
		print("Su anki yukseklik{}".format(plane.location.global_relative_frame.alt))
		time.sleep(0.5)
	print("Takeoff gerceklesti")


arm_ol_ve_yuksel(15)

plane.mode = VehicleMode("LAND")
print("İniş gerçekleşti")

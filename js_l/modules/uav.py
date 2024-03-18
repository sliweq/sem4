from albatros import Copter
from albatros.nav import PositionGPS
from albatros.enums import CopterFlightModes

import time, sys 

#lat(n,s) i lon(e,w)
targets_coordinates_gps = [(-35.36255402592787, 149.16477023825743),
     (-35.36283802041107, 149.1646026081201)]

#random altitude, but must be greater than 4, pola marsjaskie rules

FLIGHT_ALTITUDE = 5
ERROR_MARGIN = 0.2 #error margin in meters


def main():
    copter = Copter()

    copter.wait_gps_fix() 
    while not copter.set_mode(CopterFlightModes.GUIDED):
            time.sleep(3)

    #arming the copter
    while not copter.arm():
        print("Waiting for arm the copter")
        time.sleep(3)
    print("Copter is amred")

    #take off the copter
    while not copter.takeoff(FLIGHT_ALTITUDE):
        print("Unalbe to takeoff copter aborting")
        time.sleep(2)
    
    #waiting to reach the altitude
    while(current_altitude := copter.get_corrected_position().alt_m) < 4:
        print(f"Current altitiude {current_altitude} m")
        time.sleep(2)
    print(f"Current altitiude {current_altitude} m")

    #flight to points 
    copter_fly_to_gps(targets_coordinates_gps,copter)
    
    try:
        while not copter.set_mode(CopterFlightModes.RTL):
            time.sleep(1)
    except Exception:
        pass
    
    while(current_altitude := copter.get_corrected_position().alt_m) > 0.03:
        print(f"Current altitiude {current_altitude} m")
        time.sleep(3)
    print(f"Current altitiude {current_altitude} m")

def copter_fly_to_gps(array_of_coordinates, copter):
    
    for coordinates in array_of_coordinates:     
        while not copter.fly_to_gps_position(coordinates[0],coordinates[1],FLIGHT_ALTITUDE):
            time.sleep(1) 
            
        distance = copter.get_corrected_position().distance_to_point(point = PositionGPS(coordinates[0],coordinates[1]))

        while distance > ERROR_MARGIN: # or something a little greater than 0 (margin of error)

            distance = copter.get_corrected_position().distance_to_point(point = PositionGPS(coordinates[0],coordinates[1]))
            print(f"Distance to target:{distance} m")
            time.sleep(1)
        
        print(f"Copter reached target number:{targets_coordinates_gps.index(coordinates) +1}")
        
# def copter_fly_home_pos(copter):
    
#     copter.set_mode(CopterFlightModes.RTL)
    
#     distance = distance_between_points(copter.get_corrected_position(), copter.fetch_home_position())
    
#     while distance > ERROR_MARGIN: # or something a little greater than 0 (margin of error)
#         current_position = copter.get_corrected_position()
#         distance = distance_to_point(copter.fetch_home_position())
#         print(f"Distance to home:{distance} m")
#         time.sleep(1)
        
#     print("Copter reached target started position")

#     #landing
    
#     copter.set_mode(CopterFlightModes.GUIDED)
    
#     if not copter.land():
#         print("Unable to land")
#         sys.exit(1)

#     while(copter.get_corrected_position().alt_m >= 0.05):
#         print(f"Landing {copter.get_corrected_position().alt_m}")
#         time.sleep(1)

main()

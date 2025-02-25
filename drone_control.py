import CoDrone_mini
from CoDrone_mini import Direction
import pynput
from pynput import mouse, keyboard
import time

drone = CoDrone_mini.CoDrone()
user_input = input("Enter Command: ")
drone.pair()

battery_percent = drone.get_battery_percentage()
if battery_percent > 70:
    print("\nstatus: great!\n")
elif 40 < battery_percent < 70:
    print("\nstatus: good.\n")
else:
    print("\nstatus: bad...\n")

print("diagnostics\n")

print(f"battery percentage: {drone.get_battery_percentage()}")
print(f"altitude: {drone.get_altitude()}")
print(f"angle: {drone.get_angle()}")
print(f"atmospheric pressure: {drone.get_pressure()}")
print(f"internal tempurature: {drone.get_drone_temp()}")
print(f"height: {drone.get_height()}")
time.sleep(1)
print("\nGood To Go!\n")

def onclick(*args):
    x, y, button, clicked = args
    if args[-1]:
        print('{} is held down'.format(args[-2].name))

        if args[-2].name == "left":
            drone.set_yaw(30)
            print("turning left...")
            drone.move()
        
        if args[-2].name == "right":
            drone.set_yaw(-30)
            print("turning right...")
            drone.move()

    elif not args[-1]:
        print('{} is released'.format(args[-2].name))



def onpress(key):
    real_key = str(key).replace("'", "")
    if key == keyboard.Key.esc:
        return False
    
    if real_key == "t":
        print("t (taking off)")
        drone.takeoff()
    if real_key == "l":
        print("l (landing...)")
        drone.land()
        drone.close()
    if real_key == "w":
        print("w (moving forward...)")
        drone.go(Direction.FORWARD, duration= 1, power= 30)
    if real_key == "a":
        print("a (moving left...)")
        drone.go(Direction.LEFT, duration= 1, power= 30)
    if real_key == "s":
        print("s (moving back...)")
        drone.go(Direction.BACKWARD, duration= 1, power= 30)
    if real_key == "d":
        print("d (moving right...)")
        drone.go(Direction.RIGHT, duration= 1, power= 30)
    if real_key == "e":
        print("e (moving upwards...)")
        drone.go(Direction.UP, duration= 1, power= 30)
    if real_key == "q":
        print("q (moving downwards...)")
        drone.go(Direction.DOWN, duration= 1, power= 30)
    if real_key == "f":
        print("FLIPPING!!!")
        drone.flip(Direction.FORWARD)

def onrelease(key):
    print('{0} release'.format(key))
    
    # resetting commands
    drone.set_pitch(0)
    drone.set_roll(0)
    drone.set_throttle(0)
    drone.set_yaw(0)
    
with keyboard.Listener(on_press=onpress, on_release=onrelease) as key_listener, mouse.Listener(on_click=onclick) as mouse_listener:


    mouse_listener.join()
    key_listener.join()


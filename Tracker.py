from microbit import *
import radio
def scrollin(image):
  display.scroll(str(image))
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
radio.config(channel=7)
radio.on()
f = 0
b = 0
steps = 0
fc = 0
bc = 0 
receiver = 0
goal = 10;
wasgoal = 1
while True:
  accx = accelerometer.get_x()
  accy = accelerometer.get_y()
  accz = accelerometer.get_z() #get acc values
  rlz = translate(accz,-2048,2048,-180,180)
  if rlz > 25 and fc ==0 and receiver == 0:# vars to check forward swing
    f = 1
    fc = 1 
    print("f1")
  if rlz < -25 and bc == 0 and receiver == 0: # var to  check backward swing
    b = 1
    bc = 1
    print("f2")
  if f == 1 and b == 1 and receiver == 0: # if both vars are 1, steps = steps + 1 
    steps = steps + 1
    f  = 0
    b = 0
    fc = 0
    bc = 0
    print("Count")
  if steps >= goal and wasgoal == 0:
    display.show(Image.HAPPY)
    sleep(3500);
    wasgoal = 1;
    display.scroll('You hit your goal of 1000!')
  if accelerometer.was_gesture("shake")and receiver == 0: # print steps
    display.scroll(str(steps))
    radio.send(str(steps))
  if button_b.was_pressed():
    if receiver == 0:
      receiver = 1
      display.scroll('Sending.')
    elif receiver == 1:
      receiver = 0
      display.scroll('Off.')
  msg = radio.receive()
  if receiver == 1 and msg:
    scrollin(msg)

import sensor
import image
import lcd
import time
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
green_threshold   = (0,   80,  -70,   -10,   -0,   30)
while True:
    img=sensor.snapshot()
    blobs = img.find_blobs([green_threshold])
    if blobs:
    	for b in blobs:
               print("x:%d,y:%d,w:%d,h:%d"%(blob.cx(),blob.cy(),blob.w(),blob.h()))
               img.draw_rectangle(blob.rect())
               print("像素数量：%d"%blob.pixels())
    lcd.display(img)
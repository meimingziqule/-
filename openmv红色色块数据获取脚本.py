import sensor, image, time, pyb,math,lcd    
from pyb import UART, LED,Pin, Timer
# 50kHz pin6 timer2 channel1
light = Timer(2, freq=50000).channel(1, Timer.PWM, pin=Pin("P6"))
light.pulse_width_percent(50) # 控制亮度 0~100

#red_thresholds = (0, 38, 0, 124, -128, 127)# 通用红色阈值
red_thresholds = (29, 97, 14, 127, -128, 127)
roi_2 = (50,60,60,160)
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA2)   # Set frame size to QQVGA2 (128x160)
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.set_auto_gain(False) # 必须关闭自动增益以进行颜色追踪
sensor.set_auto_whitebal(False) # 必须关闭白平衡以进行颜色追踪0
clock = time.clock()

lcd.init(freq=15000000)
uart = UART(3,115200)  
uart.init(115200, bits=8, parity=None, stop=1 )
#  #1是十字路口    #2是终点

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    red_blobs = img.find_blobs([red_thresholds],roi=roi_2,x_stride=5, y_stride=5, pixels_threshold=10) 
    for blob in red_blobs:
        print("x:%d,y:%d,w:%d,h:%d"%(blob.cx(),blob.cy(),blob.w(),blob.h()))
        img.draw_rectangle(blob.rect())
        print("像素数量：%d"%blob.pixels())
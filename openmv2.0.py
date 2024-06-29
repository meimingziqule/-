import sensor, image, time, pyb,math,lcd
from pyb import UART, LED,Pin, Timer
roi_1 = (0,103,128,25)
roi_2 = (50,60,80,160)
lcd.init(freq=15000000)	
black_thresholds = (0, 75, -128, 126, -128, 127)
red_thresholds = (29, 97, 14, 127, -128, 127)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA2)
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

light = Timer(2, freq=50000).channel(1, Timer.PWM, pin=Pin("P6"))
light.pulse_width_percent(5) # 控制亮度 0~100

uart = UART(3,115200)
uart.init(115200, bits=8, parity=None, stop=1 )
while(True):
	clock.tick()
	img = sensor.snapshot()
	black_blobs = img.find_blobs([black_thresholds],x_stride=10, y_stride=10, pixels_threshold=100)
	red_blobs_1 = img.find_blobs([red_thresholds],roi=roi_1,x_stride=10, y_stride=10, pixels_threshold=800)
	red_blobs_2 = img.find_blobs([red_thresholds],roi=roi_2,x_stride=5, y_stride=5, pixels_threshold=10)
	img.draw_rectangle(roi_1, color=(0, 0, 255))
	img.draw_rectangle(roi_2, color=(0, 255, 0))
	black_blobs_num = len(black_blobs)
	if not red_blobs_1:
		print("none_#1;")
	else:
		for blob in red_blobs_1:
			img.draw_rectangle(blob.rect())
			img.draw_cross(blob.cx(), blob.cy())
			uart.write('#1;')
			pyb.delay(2000)
			img.draw_string(0, 0, "red_blobs", color=(255, 0, 0), scale=2)
			print("#1;")
	if black_blobs_num >= 5:
		if not red_blobs_2:
			uart.write('#2;')
			print("#2;")
			img.draw_string(0, 0, "black_blobs_num:", color=(255, 0, 0), scale=2)
		else:
			print('none_#2;')
	else:
		print("black_blobs_num:%d"%black_blobs_num)



	lcd.display(img)
	light = Timer(2, freq=50000).channel(1, Timer.PWM, pin=Pin("P6"))
	light.pulse_width_percent(5) # 控制亮度 0~100

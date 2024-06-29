import sensor, image, time, pyb
#初始化一次auto_roi->找到auto_roi中的红色色块并返回外接矩形框坐标->将该坐标赋值给auto_roi->由statistics得到新的颜色阈值->从第二步开始循环
red_thresholds = (47, 0, 78, 11, 65, -31)    #定义变量
auto_roi = (64,80,10,10)#第一次初始化
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA2)   # Set frame size to QVGA (128x160)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    get_auto_roi_blobs = image.find_blobs(red_thresholds, roi=auto_roi, x_stride=2, y_stride=1, invert=False, area_threshold=10, pixels_threshold=10,\
                      merge=False, margin=0, threshold_cb=None, merge_cb=None)
    img.draw_rectangle(auto_roi, color = (255,255,255))   #画roi框

    for blob in get_auto_roi_blobs:
            blob_rect = blob.rect()
            auto_roi = blob_rect

    statistics_Data = img.get_statistics(roi = (58, 122, 20, 20) )
#    print(statistics_Data)
#    print(statistics_Data.l_mode()) #LAB众数，打印出来看看效果稳定不稳定
#    print(statistics_Data.a_mode())
#    print(statistics_Data.b_mode())
    color_L_Mode = statistics_Data.l_mode()     #分别赋值LAB的众数
    color_A_Mode = statistics_Data.a_mode()
    color_B_Mode = statistics_Data.b_mode()
    #计算颜色阈值，这样写的话，颜色阈值是实时变化的，后续想要什么效果可以自己修改
    red_thresholds = (color_L_Mode-5, color_L_Mode+5, color_A_Mode-5, \
                         color_A_Mode+5, color_B_Mode-5, color_B_Mode+5)
    img.binary([red_thresholds]) #二值化看图像效果
    print(red_thresholds)        #打印输出颜色阈值
    print(clock.fps())

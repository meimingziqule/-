import image,sensor
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) ######320×240
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.run(1)
sensor.skip_frames(n=10)
while(True):
    img = sensor.snapshot()
    # 假设 img 是一个 image.Image 对象
    left, top, width, height = 100, 100, img.width(), img.height()

    # 计算除了左上角 100x100 区域以外的区域的坐标
    right = min(img.width(), left + width)
    bottom = min(img.height(), top + height)

    # 使用 img.crop() 来获取这个区域
    cropped_img = img.crop((left, top, right, bottom))
    
    # 现在 cropped_img 包含了除了原始图像左上角 100x100 区域以外的所有像素
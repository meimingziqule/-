import sensor, image, lcd, time, math
import KPU as kpu
import gc, sys
from machine import UART, Timer
from fpioa_manager import fm
###
red_threshold = (30, 100, 15, 127, 15, 127)
input_size = (224, 224)

labels = ["9", "1", "4", "2", "3", "8", "5", "6", "7"]
anchors = [0.4192, 0.3702, 0.5744, 1.6689, 0.6932, 0.6054, 1.0054, 0.9615, 2.1672, 1.6683]

num = 0
condi_flag = ""
begin_flag = 1
red_flag = 0
fm.register(18, fm.fpioa.UART1_RX, force=True)
fm.register(19, fm.fpioa.UART1_TX, force=True)
uart = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)

lcd.init(freq=15000000)

######找出列表中出现次数最多的元素
def find_most_common(list):  
    count_dict = {}
    for item in list:######遍历列表
        if item in count_dict:######如果元素已经存在于字典中，则增加计数
            count_dict[item] += 1######增加计数
        else:######如果元素不存在于字典中，则初始化计数为1
            count_dict[item] = 1######初始化计数为1
    max_count = max(count_dict.values())######找到最大计数
    most_frequent_values = [k for k, v in count_dict.items() if v == max_count]######找到所有最大计数的元素
    if len(most_frequent_values) == 1:
        return most_frequent_values[0]
    else:
        list.clear()  ###### 出现最大元素个数相同，则清空传入的列表
        return None
######获取数字识别结果
def find_most_commom_value(img,objects,num):
    if objects:
        list = []
        for obj in objects:
            pos = obj.rect()
            img.draw_rectangle(pos)
            img.draw_string(pos[0], pos[1], "%s : %.2f" %(labels[obj.classid()], obj.value()), scale=2, color=(255, 0, 0))
            print("%s : %.2f" %(labels[obj.classid()], obj.value()))
            list.append(labels[obj.classid()])######添加预测结果到列表
            num += 1
            print(num)
            if num == 10:
                print("num ==10")
                num = 0
                most_commom_value = find_most_common(list)

######位置检测
def find_num_condi(center_x,center_y):
     if center_x > 0 and center_x < 120 and center_y > 0 and center_y < 240:
         return "######0l"
     elif center_x > 180 and center_x < 320 and center_y > 0 and center_y < 240:
         return "######0r"
     else:
         return "######0c"

def find_red_blob(img,red_threshold):
    blobs = img.find_blobs([red_threshold])
    if blobs:
        return 1
    else:
        return 0
    

def is_stop(red_flag,num_flag):
    if red_flag == 1 and num_flag == 1:
        return 1
    else:
       return 0
    
def main(anchors = None,labels = None, model_addr="/sd/demo.kmodel", sensor_window=input_size, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA) ######320×240
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.set_hmirror(True)
    sensor.set_vflip(True)
    sensor.run(1)
    sensor.skip_frames(n=10)
    global num,condi_flag,begin_flag,red_threshold,red_flag
    
    try:
        task = None
        task = kpu.load(model_addr)
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) ###### threshold:[0,1], nms_value: [0, 1]
        while(True):
            img = sensor.snapshot()
            objects = kpu.run_yolo2(task, img)
            if objects:
                list = []
                for obj in objects:
                    red_flag =find_red_blob(img,red_threshold) ###### 识别红色
                    pos = obj.rect()
                    img.draw_rectangle(pos)
                    img.draw_string(pos[0], pos[1], "%s : %.2f" %(labels[obj.classid()], obj.value()), scale=2, color=(255, 255, 255))
                    center_x = pos[0] + pos[2] / 2
                    center_y = pos[1] + pos[3] / 2
                    condi_flag = find_num_condi(center_x,center_y)  ######如：######0l
                    print("%s : %.2f" %(labels[obj.classid()], obj.value()))
                    list.append(labels[obj.classid()])######添加预测结果到列表
                    num +=1
                    print(num)
                    img.draw_string(0, 100, "num:%d"%(num) , scale=2, color=(255, 255, 255))
                    if num == 25:
                        print("num ==25")
                        img.draw_string(0, 100, "num:%d"%(num) , scale=2, color=(255, 255, 255))
                        num = 0
                        most_commom_value = find_most_common(list)
                        list.clear()
                        if most_commom_value != None:######判断是否返回最大值
                            if begin_flag ==1:
                                begin_flag = begin_flag + 1
                                uart.write("######0b"+str(most_commom_value)+';')

                                print("######0b")
                                print("begin")                                                                                                                       
                            else:    
                                uart.write(str(condi_flag)+str(most_commom_value)+';')
                                img.draw_string(0, 200, "finish" , scale=2, color=(255, 255, 255))
                                print("most_commom_value:",most_commom_value)
                                print(str(condi_flag)+str(most_commom_value))
                        else:
                            print("no most_commom_value")
                            img.draw_string(0, 150, "none_finish" , scale=2, color=(255, 255, 255))

            lcd.display(img)
    except Exception as e:
        raise e
    finally:
        if not task is None:
            kpu.deinit(task)


if __name__ == "__main__":
    try:
        ###### main(anchors = anchors, labels=labels, model_addr=0x300000, lcd_rotation=0)
        main(anchors = anchors, labels=labels, model_addr="/sd/demo.kmodel")
    except Exception as e:
        sys.print_exception(e)
    finally:
        gc.collect()
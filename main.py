
from machine import Pin, SoftI2C
import ssd1306
from time import sleep
import urequests
import uasyncio
import ConnectWiFi
import PrinterInfo

quickStatsURL = "http://10.0.0.6:7125/printer/objects/query?webhooks=state&display_status=progress&virtual_sdcard=progress,is_active&print_stats=filename,print_duration,state&heater_bed=temperature,target&extruder=temperature,target"

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 32
display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
display.rotate(False)

ConnectWiFi.connect()


def draw_progress_bar(progress):
    progress_percent = int(progress*100)
    
    progress_bar_filled = int(progress * oled_width)
    
#     display.rect(0, 0, 128, 8, 0xffff)
    
    display.fill_rect(0, 0, progress_bar_filled, 8, 0xffff)
        
    
    if progress_percent > 65:
        display.text(f"{progress_percent}%", 52, 1, 0x0000)
    else:
        display.text(f"{progress_percent}%", 100, 0, 0xffff)
        
        
def printing_display(stats):
    
    eta_seconds = stats["eta"]
    
    if (eta_seconds == 0):
        eta_text = "     ..."
    else:
        minutes, seconds = divmod(eta_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        eta_text = "%01d:%02d:%02d" % (hours, minutes, seconds)
        
    
    display.fill(0)

    row2 = stats["filename"]
    row3 = eta_text
    
    screen1 = [[0, 12, row2, True], [0,24, "ETA", False], [72, 24, row3, False]]
    
    scroll_in_screen_with_static(screen1, 2, draw_progress_bar, stats["progress"])
    

def loading_display():
    display.fill(0)
    
    display.text("Loading...", 28, 12, 0xffff)
    
    display.show()

def standby_display(stats):


    extruder = f"{stats['extruder']['temperature']:.0f}/{stats['extruder']['target']:0}"
    bed = f"{stats['bed']['temperature']:.0f}/{stats['bed']['target']:0}"
    
    screen1_row1 = "Standby"
    screen1_row2 = stats['filename']
    screen1_row3_label = "Extruder"
    screen1_row3 = extruder
    screen1_row3_offset = 128-len(extruder)*8
    screen1_row4_label = "Bed"
    screen1_row4_offset = 128-len(bed)*8
    screen1_row4 = bed
    screen1 = [
        [0, 0, screen1_row1, False],
        [0, 8, screen1_row2, True],
        [0, 16, screen1_row3_label, False],
        [screen1_row3_offset, 16, screen1_row3, False],
        [0, 24, screen1_row4_label, False],
        [screen1_row4_offset, 24, screen1_row4, False]
    ]
    
    scroll_in_screen(screen1, 1)
    
def scroll_in_screen(screen, speed=1):
    for i in range (0, oled_width+1, speed):
#     for i in range (oled_width+1, 0, -speed):
        for line in screen:
            if line[3]:
                display.text(line[2], - oled_width+i, line[1])
            else:
                display.text(line[2], line[0], line[1])
        display.show()
        
        if i!= oled_width:
            display.fill(0)
                
def scroll_in_screen_with_static(screen, speed, static, args):
    for i in range (0, oled_width+1, speed):
        for line in screen:
            if line[3]:
                display.text(line[2], - oled_width+i, line[1])
            else:
                display.text(line[2], line[0], line[1])
        static(args)
        display.show()
        
        if i!= oled_width:
            display.fill(0)
            
            
def scroll_out_screen(speed):
  for i in range ((oled_width+1)/speed):
    for j in range (oled_height):
      oled.pixel(i, j, 0)
    oled.scroll(speed,0)
    oled.show()
        
def scroll_screen_in_out(screen):
    for i in range (0, (oled_width+1)*2, 1):
        for line in screen:
            if line[3]:
                display.text(line[2], - oled_width+i, line[1])
            else:
                display.text(line[2], line[0], line[1])
        display.show()
        if i!= oled_width:
            display.fill(0)
            
def scroll_in_screen_vert(screen):
  for i in range (0, (oled_height+1), 1):
    for line in screen:
      oled.text(line[2], line[0], - oled_height + i + line[1])
    display.show()
    if i!= oled_height:
      display.fill(0)
      
def scroll_out_screen_vert(speed):
  for i in range ((oled_height+1)/speed):
    for j in range (oled_width):
      display.pixel(j, i, 0)
    display.scroll(0,speed)
    display.show()
    
    
def scroll_screen_in_out_vert(screen):
  for i in range (0, (oled_height*2+1), 1):
    for line in screen:
      display.text(line[2], line[0], -oled_height+i+line[1])
    display.show()
    if i!= oled_height:
      display.fill(0)
      
async def main():
    
    loading_display()
    while True:
#         scroll_out_screen(8)
        
        stats = PrinterInfo.get_stats()
        state = stats["state"]
        
#         print(stats)
#         print(state)
        
        if (state == "standby" or state == "complete"):
            standby_display(stats)
        elif (state == "printing"):
            printing_display(stats)
        
        await uasyncio.sleep_ms(1000)
#         
#         scroll_out_screen(4)
#         
#         await uasyncio.sleep_ms(4000)
    

uasyncio.run(main())



from machine import Pin, I2C
# requires ssd1306 class, configure import depending on local structure
from modules import ssd1306, syna
from time import sleep

i2c = I2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

items = ['Test 1', 'Test 2', 'Test 3', 'Test 4', 'Test 5', 'Test 6', 'Test 7', 'Test 8', 'Test 9', 'Test 10', 'Test 11']
menu = syna.syna(oled, items, 'Testdevice')

menu.show()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

sleep(1)
menu.down()

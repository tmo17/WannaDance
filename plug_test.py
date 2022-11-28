# Additional libraries
import random

# Capactive Sensor 
import time
import board
import busio
import adafruit_mpr121
import requests
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# THIS IS FOR THE LED SCREEN
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c) # Create the SSD1306 OLED class.
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height)) # Create blank image for drawing.
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

# # LED LIGHT STRIP
# import qwiic_led_stick
# my_stick = qwiic_led_stick.QwiicLEDStick()
# red_list = [214, 78, 183, 198, 59, 134, 15, 209, 219, 186]
# green_list = [59, 216, 170, 21, 114, 63, 226, 92, 155, 175]
# blue_list = [214, 147, 25, 124, 153, 163, 188, 33, 175, 221]

# The specific capacitive sensors(aka the tiles) that will light up and need to be stepped on
column = [0,1,2,3,4,5]

# Players' points
player1 = 0
player2 = 0
plug_status = False

# String inputted will be displayed to the LCD Screen
def displayToLCD(strToDisplay):
    # LED SCREEN
    oled.fill(0) # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    draw.text((0, 0), strToDisplay, font=font, fill=255) # SET THE LED SCREEN
    oled.image(image) # Display image
    oled.show() # show all the changes we just made

# Checks if user stepped on a tile and gives them points if they did
def checkTile(tile_to_tap):
    global player1
    global player2
    global plug_status
    
    time.sleep(5) # Give users time to step on a tile 
    if mpr121[tile_to_tap[0]].value == True and mpr121[tile_to_tap[1]].value == True:
        print("Toggle plug")
        plug_status = not plug_status

        PARAMS = {}
        toggle_URL = 'http://192.168.0.138/cm?cmnd=Power%20TOGGLE'
        # sending get request and saving the response as response object
        r = requests.get(url = toggle_URL)
        
        # extracting data in json format
        data = r.json()
        print(data)
        
        

# Main game loop ran here
def game():
    global player1
    global player2
    global plug_status

    plug_status = False
    while True:
        displayToLCD(f"Player1: {player1}\n Player2: {player2}")
        # my_stick.set_all_LED_color(214, 0, 0)
        tile_to_tap = [0,11]
        checkTile(tile_to_tap)



# Game initialization and ending done here
def main():
    # LED LIGHT STRIP SETUP
    # if my_stick.begin() == False:
    #     print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", file=sys.stderr)
    #     return
    # print("\nLED Stick ready!")

    # Start the game
    winner = game()

if __name__ == "__main__":
    main()
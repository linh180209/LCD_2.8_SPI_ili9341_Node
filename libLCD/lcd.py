import sys
import json
import Image
import ImageDraw
import ImageFont
import Image

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# BeagleBone Black configuration.
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0

# Raspberry Pi configuration.
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

BEGIN = "begin"
CLEAR = "clear"
TEXT = "text"
TEXT_POSITION = "text_position"
DISPLAY = "display"
DISPLAYIMAGE = "displayImage"
EXIT = "exit"

wscreen = 240
hscreen = 320

class objectText(object):
    """docstring for objectText"""
    def __init__(self, text, x, y):
        super(objectText, self).__init__()
        self.text = text
        self.x = x
        self.y = y

def ProcessHCENTER(text, spaceline, rotate, fontname, size):
    global wscreen,hscreen
    ArrayText = []
    if rotate == 0:
        wscreen = 240
        hscreen = 320
    elif rotate == 90:
        wscreen = 320
        hscreen = 240
    font = ImageFont.truetype(fontname, size)
    (wText,hText) = font.getsize(text)
    
    if (wText < wscreen):
        x = (wscreen-wText)/2
        y = 0
        print("x: %d, y: %d"%(x,y))
    else:
        words = text.split(" ")
        print("size: %d"%len(words))    
        if(len(words) > 1):
            while len(words) > 0:
                no = 0
                textTemp = ""
                for i in range(0,len(words)):
                    if(i != 0):
                        textTemp = textTemp + " " + words[i]
                    else:
                        textTemp = textTemp + words[i]
                    (w,h) = font.getsize(textTemp)
                    if w < wscreen:
                        no = i
                    else:
                        break

                print("no: %d"%no)
                t = ""
                for k in range(0,no+1):
                    w = words.pop(0)
                    if(k != 0):
                        t = t + " " + w
                    else:
                        t = t + w
                print("text: " + t)
                space = 0
                if len(ArrayText) > 0:
                    space = spaceline*(len(ArrayText))
                (w,h) = font.getsize(t)
                print("w: %d,h: %d"%(w,h))
                x = (wscreen-w)/2 
                y = h*len(ArrayText) + space
                print("x: %d, y: %d"%(x,y))
                temp = objectText(t,x,y)
                ArrayText.append(temp)
        else:
            words = text
            print("size: %d"%len(words))    
            if(len(words) > 1):
                while len(words) > 0:
                    no = 0
                    textTemp = ""
                    for i in range(0,len(words)):
                        if(i != 0):
                            textTemp = textTemp + " " + words[i]
                        else:
                            textTemp = textTemp + words[i]
                        (w,h) = font.getsize(textTemp)
                        if w < wscreen:
                            no = i
                        else:
                            break

                    print("no: %d"%no)
                    t = ""
                    for k in range(0,no+1):
                        w = words[0]
                        words = words[1:]
                        if(k != 0):
                            t = t + w
                        else:
                            t = t + w
                    print("text: " + t)
                    space = 0
                    if len(ArrayText) > 0:
                        space = spaceline*(len(ArrayText))
                    (w,h) = font.getsize(t)
                    print("w: %d,h: %d"%(w,h))
                    x = (wscreen-w)/2 
                    y = h*len(ArrayText) + space
                    print("x: %d, y: %d"%(x,y))
                    temp = objectText(t,x,y)
                    ArrayText.append(temp)
    return ArrayText
def ProcessVCENTER(text, spaceline, rotate, fontname, size):
    global wscreen,hscreen
    if rotate == 0:
        wscreen = 240
        hscreen = 320
    elif rotate == 90:
        wscreen = 320
        hscreen = 240
    font = ImageFont.truetype(fontname, size)
    (wText,hText) = font.getsize(text)
    arrayText = ProcessHCENTER(text, spaceline, rotate, fontname, size)
    maxH = 0
    for t in arrayText:
        if t.y > maxH:
            maxH = t.y

    if maxH > hscreen:
        return arrayText
    else:
        offset = (hscreen - maxH - hText)/2
        for t in arrayText:
            t.y = t.y + offset
            t.x = 0
    return arrayText

def ProcessVCENTER_HCENTER(text, spaceline, rotate, fontname, size):
    global wscreen,hscreen
    if rotate == 0:
        wscreen = 240
        hscreen = 320
    elif rotate == 90:
        wscreen = 320
        hscreen = 240
    font = ImageFont.truetype(fontname, size)
    (wText,hText) = font.getsize(text)
    arrayText = ProcessHCENTER(text, spaceline, rotate, fontname, size)
    maxH = 0
    for t in arrayText:
        if t.y > maxH:
            maxH = t.y

    if maxH > hscreen:
        return arrayText
    else:
        offset = (hscreen - maxH - hText)/2
        for t in arrayText:
            t.y = t.y + offset
    return arrayText
        
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)

def genera_position(text, wText, hText, position, spaceline, rotate, fontname, size):
    if(position == "HCENTER"):
        arrayText = ProcessHCENTER(text, spaceline, rotate, fontname, size)

    elif(position == "VCENTER"):
        arrayText = ProcessVCENTER(text, spaceline, rotate, fontname, size)

    elif(position == "HCENTER&VCENTER"):
        arrayText = ProcessVCENTER_HCENTER(text, spaceline, rotate, fontname, size)

    return arrayText

if __name__ == '__main__':
    while True:
        data = raw_input()
        print data
        d = json.loads(data)
        command = d["command"]
        if(command == EXIT): #{"command":"exit"}
            print("python: exit")
            break

        elif(command == BEGIN): #{"command":"begin"}
            print("python begin")
            # Create TFT LCD display class.
            disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
            # Initialize display.
            disp.begin()

        elif(command == CLEAR): #{"command":"clear","red":102, "green":102, "blue":102}
            print("python clear: " + data)
            red = d["red"]
            green = d["green"]
            blue = d["blue"]
            disp.clear((red, green, blue))

        elif(command == TEXT): #{"command":"text","text":"hello","position":{"x":150,"y":120,"rotate":90},"font":{"name":"Minecraftia.ttf","size":16,"red":255,"green":255,"blue":255}}
            print("python text: " + data)
            # Load default font.
            name = d["font"]["name"]
            if(name == "default"):
                font = ImageFont.load_default()
            else:
                size = d["font"]["size"]
                font = ImageFont.truetype(name, size)
            
            text = d["text"]
            x = d["position"]["x"]
            y = d["position"]["y"]
            rotate = d["position"]["rotate"]
            red = d["font"]["red"]
            green = d["font"]["green"]
            blue = red = d["font"]["blue"]
            draw_rotated_text(disp.buffer, text, (x, y), rotate, font, fill=(red,green,blue))

        elif(command == TEXT_POSITION):
            name = d["font"]["name"]
            if(name == "default"):
                font = ImageFont.load_default()
            else:
                size = d["font"]["size"]
                font = ImageFont.truetype(name, size)
            
            text = d["text"]
            (wText,hText) = font.getsize(text)
            position = d["position"]["position"]
            spaceline = d["position"]["spaceline"]
            rotate = d["position"]["rotate"]
            red = d["font"]["red"]
            green = d["font"]["green"]
            blue = red = d["font"]["blue"]
            arrayText = genera_position(text, wText, hText, position, spaceline, rotate, name, size)
            for t in arrayText:
                draw_rotated_text(disp.buffer, t.text, (t.x, t.y), rotate, font, fill=(red,green,blue))

        elif(command == DISPLAY):#{"command":"display"}
            print("python display")
            disp.display()

        elif(command == DISPLAYIMAGE):#{"command":"displayImage","imagename":"picture.jpg","rotate":90,"width":width,"height":height}
            print("python display image")
            imagename = d["imagename"]
            rotate = d["rotate"]
            width = d["width"]
            height = d["height"]
            image = Image.open(imagename)
            # Resize the image and rotate it so it's 240x320 pixels.
            image = image.rotate(rotate).resize((width, height))
            disp.display(image)



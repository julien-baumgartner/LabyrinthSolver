import cv2
import numpy as np
import time

class Pixel:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        if(parent == None):
            self.value = 0
        else:
            self.value = parent.value+1

    def isEquals(self, pixel):
        return (self.x == pixel.x and self.y == pixel.y)

def findPath(start, end, img):

    queuePixels = []
    queuePixels.append(Pixel(start[0], start[1]))

    fini = False
    etape = 0
    while(len(queuePixels) > 0 and fini == False):
        etape = etape + 1
        pixel = queuePixels.pop(0)

        nbNewPixels = 0
        if(pixel.x == end[0] and pixel.y == end[1]):
            lastPixel = pixel
            #print("VICTORY")
            fini = True
        else:
            newPixel = Pixel(pixel.x-1, pixel.y, pixel)
            if(isPixelOk(newPixel, img, queuePixels)):
                queuePixels.append(newPixel)
                #print("add")

            newPixel = Pixel(pixel.x+1, pixel.y, pixel)
            if(isPixelOk(newPixel, img, queuePixels)):
                queuePixels.append(newPixel)
                #print("add")

            newPixel = Pixel(pixel.x, pixel.y-1, pixel)
            if(isPixelOk(newPixel, img, queuePixels)):
                queuePixels.append(newPixel)
                #print("add")

            newPixel = Pixel(pixel.x, pixel.y+1, pixel)
            if(isPixelOk(newPixel, img, queuePixels)):
                queuePixels.append(newPixel)
                #print("add")


        img[pixel.x, pixel.y, 0] = 0
        img[pixel.x, pixel.y, 1] = 0
        img[pixel.x, pixel.y, 2] = 0
        #sorted(queuePixels, key=lambda pixel: pixel.value)
        #if etape % 10000 == 0:
            #cv2.imshow('Input', img)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

    path = []

    if(fini == True):
        while(lastPixel.parent != None):
            path.append(lastPixel)
            lastPixel = lastPixel.parent

    return path, fini

def isPixelOk(pixel, img, queuePixels):
    if(isWall(img, pixel.x, pixel.y) == False):
        if pixel.parent.parent != None and pixel.isEquals(pixel.parent.parent):
            return False
        for pix in queuePixels:
            if pixel.isEquals(pix):
                return False

        return True

    return False

def isWall(img, x, y):
    if(x < 0 or x >= height or y < 0 or y >= width):
        #print("dehors")
        return True
    #if img.item(x,y,0) != ground[0] or img.item(x,y,1) != ground[1] or img.item(x,y,2) != ground[2]:
    if abs(img.item(x,y,0) - ground[0]) > tolerence or abs(img.item(x,y,1) - ground[1]) > tolerence or abs(img.item(x,y,2) - ground[2]) > tolerence:
        #print("mur")
        return True
    return False

def detectStartEndWithColor(img):
    for w in range(width):
        for h in range(height):
            if img.item(h,w,0) == 255 and img.item(h,w,1) == 0 and img.item(h,w,2) == 0:
                end = [h,w]
                img[end[0],end[1], 1] = 255
                img[end[0],end[1], 2] = 255
            elif img.item(h,w,0) == 0 and img.item(h,w,1) == 0 and img.item(h,w,2) == 255:
                start = [h,w]
                img[start[0],start[1], 0] = 255
                img[start[0],start[1], 1] = 255
    return start, end

def isColorEquals(color1, color2):
    return abs(color1[0] - color2[0]) < tolerence and abs(color1[1] - color2[1]) < tolerence and abs(color1[2] - color2[2]) < tolerence

def convertColorChangeToPos(i):
    if i < width:
        return [0, i]
    i -= width-1
    if i < height:
        return [i, width-1]
    i -= height-1
    if i < width:
        return [height-1, width-i-1]
    i -= width-1
    return [height-i-1, 0]

def detectStartEndWithBorder(img):
    x = 0
    y = 0
    i = 0
    previousColor = [img.item(0,0,0),img.item(0,0,1),img.item(0,0,2)]
    colorChange = []
    while x < width:
        newColor = [img.item(y,x,0),img.item(y,x,1),img.item(y,x,2)]
        if not isColorEquals(previousColor, newColor):
            colorChange.append(i)
        previousColor = newColor
        x+=1
        i+=1

    x-=1
    y+=1
    while y < height:
        newColor = [img.item(y,x,0),img.item(y,x,1),img.item(y,x,2)]
        if not isColorEquals(previousColor, newColor):
            colorChange.append(i)
        previousColor = newColor
        y+=1
        i+=1

    y-=1
    x-=1
    while x >= 0:
        newColor = [img.item(y,x,0),img.item(y,x,1),img.item(y,x,2)]
        if not isColorEquals(previousColor, newColor):
            colorChange.append(i)
        previousColor = newColor
        x-=1
        i+=1

    x+=1
    y-=1
    while y >= 0:
        newColor = [img.item(y,x,0),img.item(y,x,1),img.item(y,x,2)]
        if not isColorEquals(previousColor, newColor):
            colorChange.append(i)
        previousColor = newColor
        y-=1
        i+=1

    start = convertColorChangeToPos(colorChange[0])
    end = convertColorChangeToPos(colorChange[2])

    return start, end

img = cv2.imread("images/04-3.jpg")
startTime = (int)(time.time() * 1000)
tolerence = 150
#kernel = np.ones((21,21), np.uint8) #im1
#kernel = np.ones((4,4), np.uint8) #im2
kernel = np.ones((8,8), np.uint8) #im4-3
#kernel = np.ones((16,16), np.uint8) #im6

img_erosion = cv2.erode(img, kernel, iterations=1)
img_erosionCopy = img_erosion.copy()

start = [-1, -1]
end = [-1, -1]

height, width = img.shape[:2]

#start, end = detectStartEndWithColor(img)
start, end = detectStartEndWithBorder(img_erosion)

print(start)
print(end)
ground = [img.item(start[0],start[1],0),img.item(start[0],start[1],1),img.item(start[0],start[1],2)]
#img_erosion[start[0],start[1], 2] = 0
#img_erosion[start[0],start[1], 1] = 0
#img_erosion[end[0],end[1], 0] = 0
#img_erosion[end[0],end[1], 1] = 0

cv2.imwrite('erode.png', img_erosion)

path = []
fini = False
i = 0
listTolerences = [0,10,25,50,75,100,125,150,200]
while not fini and i < len(listTolerences):
    tolerence = listTolerences[i]
    path, fini = findPath(start, end, img_erosion)
    i += 1
    img_erosion = img_erosionCopy.copy()
endTime = (int)(time.time() * 1000)

print(str(endTime - startTime) + " ms")


if(len(path) > 0):
    for pixel in path:
        img[pixel.x, pixel.y, 0] = 0
        img[pixel.x, pixel.y, 1] = 0
        img[pixel.x, pixel.y, 2] = 255

cv2.imwrite('result.png', img)
cv2.imshow('Input', img)
cv2.imshow('Erosion', img_erosion)


cv2.waitKey(0)
cv2.destroyAllWindows()

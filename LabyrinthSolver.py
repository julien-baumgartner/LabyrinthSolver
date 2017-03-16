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

    return path

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
    if img.item(x,y,0) != 255 and img.item(x,y,1) != 255 and img.item(x,y,2) != 255:
        #print("mur")
        return True
    return False

img = cv2.imread("images/02.png")
startTime = (int)(time.time() * 1000)

#kernel = np.ones((21,21), np.uint8) #im1
kernel = np.ones((4,4), np.uint8) #im2
#kernel = np.ones((16,16), np.uint8) #im6


start = [-1, -1]
end = [-1, -1]

height, width = img.shape[:2]
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

print(start)
print(end)

img_erosion = cv2.erode(img, kernel, iterations=1)

#img_erosion[start[0],start[1], 2] = 0
#img_erosion[start[0],start[1], 1] = 0
#img_erosion[end[0],end[1], 0] = 0
#img_erosion[end[0],end[1], 1] = 0

path = []
path = findPath(start, end, img_erosion)
endTime = (int)(time.time() * 1000)

print(str(endTime - startTime) + " ms")

#cv2.imwrite('erode.png', img_erosion)

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

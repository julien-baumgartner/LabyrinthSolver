import cv2
import numpy as np

class Pixel:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        if(parent == None):
            self.value = 0
        else:
            self.value = parent.value+1

def findPath(start, end, img):

    pixelsParcourus = []
    queuePixels = []
    queuePixels.append(Pixel(start[0], start[1]))

    fini = False

    while(len(queuePixels) > 0 and fini == False):

        pixel = queuePixels.pop(0)

        if(pixel.x == end[0] and pixel.y == end[1]):
            lastPixel = pixel
            fini = True
            print("VICTORY")
        else:
            newPixel = Pixel(pixel.x-1, pixel.y, pixel)
            if(isPixelOk(newPixel, img, queuePixels, pixelsParcourus)):
                queuePixels.append(newPixel)
                #print("add")

            newPixel = Pixel(pixel.x+1, pixel.y, pixel)
            if(isPixelOk(newPixel, img, queuePixels, pixelsParcourus)):
                queuePixels.append(newPixel)
                #print("add")

            newPixel = Pixel(pixel.x, pixel.y-1, pixel)
            if(isPixelOk(newPixel, img, queuePixels, pixelsParcourus)):
                queuePixels.append(newPixel)
                #print("add")

            newPixel = Pixel(pixel.x, pixel.y+1, pixel)
            if(isPixelOk(newPixel, img, queuePixels, pixelsParcourus)):
                queuePixels.append(newPixel)
                #print("add")

        pixelsParcourus.append(pixel)

        img[pixel.x, pixel.y, 0] = 0
        img[pixel.x, pixel.y, 1] = 0
        sorted(queuePixels, key=lambda pixel: pixel.value)
        #print(len(pixelsParcourus))
        if(len(pixelsParcourus) % 2000 == 0):
            cv2.imshow('Input', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    path = []

    if(fini == True):
        while(lastPixel.parent != None):
            path.append(lastPixel)
            lastPixel = lastPixel.parent

    return path

def isPixelOk(pixel, img, queuePixels, pixelsParcourus):
    if(isWall(img, pixel.x, pixel.y) == False):
        for pix in queuePixels:
            if pix.x == pixel.x and pix.y == pixel.y:
                #print("queue")
                return False
        for pix in pixelsParcourus:
            if pix.x == pixel.x and pix.y == pixel.y:
                #print("parcours")
                return False

        #print("pixel ok")
        return True

    return False

def isWall(img, x, y):
    #print(img[x,y])
    if(x < 0 or x >= 745 or y < 0 or y >= 560):
        return True
    if img.item(x,y,0) != 255 and img.item(x,y,1) != 255 and img.item(x,y,2) != 255:
            #print("wall pas ok")
        return True
    return False

img = cv2.imread("images/01.png")

kernel = np.ones((21,21), np.uint8)


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

path = [] #findPath(start, end, img_erosion)

cv2.imwrite('eee.png', img_erosion)

if(len(path) > 0):
    for pixel in path:
        img[pixel.x, pixel.y, 0] = 0
        img[pixel.x, pixel.y, 1] = 0
        img[pixel.x, pixel.y, 2] = 255

cv2.imshow('Input', img)
cv2.imshow('Erosion', img_erosion)


cv2.waitKey(0)
cv2.destroyAllWindows()

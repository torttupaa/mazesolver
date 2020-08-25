from PIL import Image
import cv2
import numpy as np
import time

ALK = True
LOP = True

visual1 = False
visual2 = False
vis = input("visual solve k/e?: ")
##vis2 = input("visual draw k/e?: ")
if vis == "k":
    visual1 = True
if vis == "k":
    visual2 = True

while ALK or LOP:
    imagename = input("Mazekuvatiedosto?: ")
    try:
        im = Image.open(imagename)

        # Get the size of the image
        width, height = im.size
        newim = Image.new(im.mode, im.size)



        #alukoord
        alku = (0,0)
        maali = (0,0)
        for x in range(width):
            for y in range(height):
                current_color = im.getpixel((x,y))
                if current_color == 113:
                    alku = (x,y+1)
                    print("Alkupiste loydetty",alku)
                    ALK = False
                if current_color == 210:
                    maali = (x, y)
                    print("Maali loydetty", maali)
                    LOP = False
                newim.putpixel((x,y), current_color)

        maalireitit = []
        reitit = [[alku]]
    except:
        print("nogood!")
newim.putpixel((alku), 150)
looppi = True


pix = newim.load()

input("Press enter to continue")
start = time.time()
print("Etsitaan reitti....")
cnt1 = 0
while looppi:
    cnt1+=1
    if len(reitit) == 0:
        break
    uudetreitit = []
    #print(len(reitit))
    for path in range(len(reitit)):
        tarkastelu = reitit[path][-1]

        oiekeelle = (tarkastelu[0]+1,tarkastelu[1])
        vasemmalle = (tarkastelu[0]-1,tarkastelu[1])
        alas = (tarkastelu[0],tarkastelu[1]+1)
        ylos = (tarkastelu[0],tarkastelu[1]-1)


        if  pix[alas[0],alas[1]] == 255:
            newpath = []
            newpath += reitit[path]
            newpath.append(alas)
            uudetreitit.append(newpath)
            pix[alas[0],alas[1]] = 150


        if pix[ylos[0], ylos[1]] == 255:
            newpath = []
            newpath += reitit[path]
            newpath.append(ylos)
            uudetreitit.append(newpath)
            pix[ylos[0], ylos[1]] = 150

        if pix[oiekeelle[0], oiekeelle[1]] == 255:
            newpath = []
            newpath += reitit[path]
            newpath.append(oiekeelle)
            uudetreitit.append(newpath)
            pix[oiekeelle[0], oiekeelle[1]] = 150

        if pix[vasemmalle[0], vasemmalle[1]] == 255:
            newpath = []
            newpath += reitit[path]
            newpath.append(vasemmalle)
            uudetreitit.append(newpath)
            pix[vasemmalle[0], vasemmalle[1]] = 150

        if oiekeelle == maali:
            maalireitit.append(reitit[path])
            looppi = False

    if visual1 and cnt1%50==0:
        img_np = np.array(newim)
        frame = cv2.resize(img_np, (width, height),interpolation=cv2.INTER_NEAREST)
        cv2.imshow("mazeLOL", frame)

        if cv2.waitKey(1) == 27:
            break
    reitit = uudetreitit
    #time.sleep(0.1)
    #print(reitit)


#print(maalireitit)
edellinen = 100000000
lyhyin = []


for ret in maalireitit:
    if len(ret) <= edellinen:
        edellinen = len(ret)
        lyhyin = ret
print("Etsinta aika: ", round((time.time()-start),3),"s")

print("Reitin pituus: ",len(lyhyin),"pixelia")


for x in range(width):
    for y in range(height):
        current_color = im.getpixel((x, y))
        pix[x, y] = current_color


start = time.time()
#print("Piirretaan reitti")
newim = newim.convert("RGB")
pix = newim.load()
counter = 0
for osa in lyhyin:
    pix[osa[0], osa[1]] = 0,0,255
    counter += 1
    if visual2 and counter%20==0:
        img_np = np.array(newim)
        frame = cv2.resize(img_np, (width, height),interpolation=cv2.INTER_NEAREST)
        cv2.imshow("mazeLOL", frame)

        if cv2.waitKey(1) == 27:
            break

#print("Piirtoaika: ", round((time.time()-start),3),"s")
newim.save('newim.png')


cv2.imshow("mazeLOL", frame)
cv2.waitKey(0)




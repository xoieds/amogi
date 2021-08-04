import os
import time
from multiprocessing import Process
import multiprocessing
from PIL import Image

# todo: multi-threading a frame on each thread
#       neat gui with size options
#       functions to split videos and gifs into frames for procesing.

add = Image.open(r"am2.jpg")


def rendfram(base, addit, fln):
    fin = Image.new('RGB', (base.width * addit.width, base.height * addit.height))
    for x2 in range(base.width):
        print(fln + " progress: ", x2 + 1, " / ", base.width)
        for y2 in range(base.height):
            for x in range(addit.width):
                for y in range(addit.height):
                    try:
                        n = (int((addit.getpixel((x, y)))[0] * ((base.getpixel((x2, y2)))[0])/255), int((addit.getpixel((x, y)))[1] * ((base.getpixel((x2, y2)))[1])/255), int((addit.getpixel((x, y)))[2] * ((base.getpixel((x2, y2)))[2])/255))
                        fin.putpixel(((x2+1*x+1) + (addit.width*x2)-1*x2, (y2+1*y+1) + (addit.height*y2)-1*y2), n)
                    except:
                        pass

    if not os.path.exists("doneframes/"):
        os.makedirs("doneframes/")
    fin.save("doneframes/" + fln)
    print("image saved to: doneframes/" + fln)
    return 0


def multip(it, szm):
    start = time.time()
    procs = []
    proc = Process(target=rendfram)
    procs.append(proc)
    proc.start()
    mpl = []

    for filename in os.listdir("frams"):
        f = os.path.join("frams", filename)
        if os.path.isfile(f):
            print(f)
            basef = Image.open(f)
            basef = basef.resize((round(basef.size[0] * szm), round(basef.size[1] * szm)))
            proc = Process(target=rendfram, args=(basef, it, filename))
            procs.append(proc)
            proc.start()

    for proc in procs:
        proc.join()

    end = time.time()
    print('Time taken in seconds : ', end - start)


while 1:
    i = input("Single frame or multiple frames in the /frames folder (s/m) ")
    if i=="s":
        while 1:
            b = input("Enter base image name: ")
            if os.path.exists(b):
                base = Image.open(b)
                break
        while 1:
            n = input("Enter iterator image name: ")
            if os.path.exists(n):
                it = Image.open(n)
                break
        imn = input("enter final image name: ")
        rendfram(base, it, imn + ".jpg")


    if i == "m":
        mpe = input("enable multiprocessing? (y/n) ")
        if mpe == "y":
            while 1:
                n = input("Enter iterator image name: ")
                if os.path.exists(n):
                    it = Image.open(n)
                    break

            sz = input("Enter base frame size multiplier: ")

            #it = Image.open("am2.jpg")

            #multip(it, 0.5)

            multip(it, float(sz))

        if mpe == "n":
            while 1:
                n = input("Enter iterator image name: ")
                if os.path.exists(n) == True:
                    it = Image.open(n)
                    break

            sz = float(input("Enter base frame size multiplier: "))
            for filename in os.listdir("frams"):
                f = os.path.join("frams", filename)
                if os.path.isfile(f):
                    print(f)
                    basef = Image.open(f)
                    basef = basef.resize((round(basef.size[0] * sz), round(basef.size[1] * sz)))
                    rendfram(basef, it, filename)


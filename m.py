import os
import time
from multiprocessing import Process
from PIL import Image

# todo: multi-threading a frame on each thread
#       neat gui with size options
#       functions to split videos and gifs into frames for procesing

add = Image.open(r"am2.jpg")


def rendfram(base, addit, fln):
    fin = Image.new('RGB', (base.width * addit.width, base.height * addit.height))
    for x2 in range(base.width):
        print("progress: ", x2, " / ", base.width)
        for y2 in range(base.height):
            for x in range(addit.width):
                for y in range(addit.height):
                    try:
                        n = (int((addit.getpixel((x, y)))[0] * ((base.getpixel((x2, y2)))[0])/255), int((addit.getpixel((x, y)))[1] * ((base.getpixel((x2, y2)))[1])/255), int((addit.getpixel((x, y)))[2] * ((base.getpixel((x2, y2)))[2])/255))
                        fin.putpixel(((x2+1*x+1) + (addit.width*x2)-1*x2, (y2+1*y+1) + (addit.height*y2)-1*y2), n)
                    except:
                        pass
    n = "donefrmas/" + fln
    fin.save(n)
    return 0


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
        mf = 0.04
        basef = basef.resize((round(basef.size[0] * mf), round(basef.size[1] * mf)))
        proc = Process(target=rendfram, args=(basef, add, filename))
        procs.append(proc)
        proc.start()

for proc in procs:
    proc.join()

end = time.time()
print('Time taken in seconds : ', end - start)

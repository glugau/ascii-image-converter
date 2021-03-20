from PIL import Image
import sys
import threading
import imghdr

INPUT_PATH = "input.jpg"
OUTPUT_PATH = "output.txt"
CHARACTERS_LIGHTMODE = "@%#*+=-:. "
CHARACTERS_DARKMODE = " .:-=+*#%@"
DARKMODE = True
THREAD_COUNT = 12

im_dimensions = [None, None]

def chunks(l, n):
    n = max(1, n)
    return [l[i * n:(i + 1) * n] for i in range((len(l) + n - 1) // n )] 


args = sys.argv
if len(args) > 1:
    try:
        fmt = imghdr.what(args[1])
        if fmt is not None:
            INPUT_PATH = args[1]
        else:
            print("Invalid input file!")
            sys.exit()
    except:
        print("Input file not found!")
        sys.exit()
    if len(args) > 2:
        OUTPUT_PATH = args[2]
        if len(args) == 5:
            try:
                im_dimensions[0] = int(args[3])
                im_dimensions[1] = int(args[4])
            except:
                print("Invalid image dimensions!")
                sys.exit()
        if len(args) == 4 or len(args) > 5:
            print("Invalid amount of parameters. Please use 'python main.py <input> <output> <width> <height>'.")
    elif len(args) > 3:
        print("Too many arguments! Use 'python main.py <input> <output> <width> <height>' to choose your input and output file.")
        sys.exit()

try:
    im = Image.open(INPUT_PATH) # opening the image in greyscale
    for i in range(len(im_dimensions)):
        if im_dimensions[i] is None:
            im_dimensions[i] = im.size[i]
    im = im.resize(im_dimensions, Image.ANTIALIAS).convert("LA")

except Exception as e:
    print(f"Image {INPUT_PATH} not found! Use 'python main.py <input> <output> <width> <height>' to choose your input and output files.")
    sys.exit()

pixels = chunks(list(im.getdata()), im.size[0]) # 2d list of the image, with each value being (color, alpha)

output_lines = []
for i in range(im.size[1]):
    output_lines.append("")

def threaded_generate(lst, startindex):
    curr = startindex
    for i in lst:
        result = ""
        for j in i:
            val = j[0] / 255 # color from 0 - 255 normalized
            chars = None
            if DARKMODE:
                chars = CHARACTERS_DARKMODE
            else:
                chars = CHARACTERS_LIGHTMODE
            index = round(val * (len(chars) - 1))
            result += chars[index]
        output_lines[curr] = result
        curr += 1

thread_pixels = chunks(pixels, len(pixels) // THREAD_COUNT)
x = 0
threads = []
for i in thread_pixels:
    t = threading.Thread(target=threaded_generate, args=(i,x))
    t.start()
    threads.append(t)
    x += len(i)

for thread in threads:
    thread.join()

output_string = "\n".join(output_lines)
with open(OUTPUT_PATH, "w+") as f:
    f.write(output_string)
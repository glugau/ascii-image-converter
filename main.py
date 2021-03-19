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
    if len(args) == 3:
        OUTPUT_PATH = args[2]
    elif len(args) > 3:
        print("Too many arguments! Use 'python main.py <input> <output>' to choose your input and output file.")
        sys.exit()

try:
    im = Image.open(INPUT_PATH).resize((50, 25), Image.ANTIALIAS).convert("LA") # opening the image in greyscale
except Exception as e:
    print(f"Image {INPUT_PATH} not found! Use 'python main.py <input> <ouput>' to choose your input and output files.")
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
            index = round(val * (len(chars)))
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
# Ascii art generator
This repo is a simple one file ascii art generator with all the functionality needed and very fast as it is multithreaded.

To use this, download the main.py file and type in your terminal

    pip install Pillow
This is, if you have a correct Python 3 installation, the only required dependency install.

After that, to use the program, go to the folder which you downloaded the file to, open your terminal and type

    python main.py <input> <output> <width> <height>

 - input: the path to the input file (image). The default value is input.jpg
 - output: the path to the output file (text). The default value is output.txt
 - width: the width of the output in characters. Defaults to the image's width
 - height: the height of the output in characters. Defaults to the image's height
 
You must type all previous arguments to type the next one, for example, you cannot choose the width without choosing the input and output paths.

There are 2 additional settings "hidden" in the code: 

 - If you edit the main.py file, you can change DARKMODE to True or False. True means that the bigger characters like # or @ represent white in the image (when turned black and white), and false means that those characters represent black.
 
 - You can also edit THREAD_COUNT to choose how many threads (in addition to the main thread) run at the same time. They each loop over a portion of the image and transform the pixels into ascii characters. They are then joined together to get an output.

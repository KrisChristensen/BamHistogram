##########################################################
### Import Necessary Modules

import argparse                       #provides options at the command line
import sys                       #take command line arguments and uses it in the script
import gzip                       #allows gzipped files to be read
import re                       #allows regular expressions to be used
import textwrap                       #allows the use of textwrapping for long sequences

"""
This script is meant to be called from another script.  It generates windows.
"""

def Window(s, e, w, st):      
    windows = []
    end = int(s) + int(w) - 1
    while int(end) < int(e):
        start = s
        end = int(s) + int(w) - 1
        if int(end) > int(e):
            end = int(e) 
        windows.append("{}:{}".format(start, end))
        s = int(s) + int(st)
    return (windows)

if __name__ == '__main__':
    start = 1
    end = 10000
    window_size = 1000
    step = 100
    windowlist = Window(start, end, window_size, step)    
    print (windowlist)

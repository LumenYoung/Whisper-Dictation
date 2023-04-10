#!/usr/bin/python
import os

# function type: run ydotool to type the given content
def type_content(content):
    os.system(f"ydotool type '{content}'")

if __name__ == "__main__":
    type_content("Hello world to the better future")
#!/usr/local/bin/python3
import argparse
import re
import shutil
import os

def change_directory(directory):
    try:
        os.chdir(directory)
        return True
    except OSError as e:
        print("Error: <{}> is not a valid directory.".format(e.filename))
        return False

def test_regular(regular=r"([a-zA-Z]+)-?(\d+[a-zA-Z]?)\.(\S+)"):
    for each in os.listdir():
        if re.match(regular, each):
            tmp = re.findall(regular, each)
            prefix = tmp[0][0].lower()
            serial = tmp[0][1]
            postfix = tmp[0][2]
            name = prefix + "-" + serial + "." + postfix
            print("will rename from <{}> to <{}>".format(each, name))
        else:
            print(">>> {} not matched".format(each))

def rename(regular=r"([a-zA-Z]+)-?(\d+[a-zA-Z]?)\.(\S+)"):
    for each in os.listdir():
        tmp = re.findall(regular, each)
        try:
            prefix = tmp[0][0].lower()
            serial = tmp[0][1]
            postfix = tmp[0][2]
            name = prefix + "-" + serial + "." + postfix
            shutil.move(each, name)
            print("rename from <{}> to <{}>".format(each, name))
        except IndexError as _:
            print(">>> {} not matched".format(each))
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--regular", help="regular expression will be used")
    parser.add_argument("-d", "--directory", help="directory you want to run the program")
    parser.add_argument("-e", "--execute", help="after debug execute the rename program", action="store_true")
    args = parser.parse_args()

    if args.directory:
    	change_directory(args.directory)

    if args.execute:
       rename()
    else:
        if args.regular:
            test_regular(args.regular)
        else:
            test_regular()

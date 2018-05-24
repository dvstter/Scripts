#!/usr/local/bin/python3
import argparse
import re
import shutil
import os

AV_PATTERN = r"([a-zA-Z]+)-?(\d+[a-zA-Z]?)\.(\S+)"
AV_REPL= r"\1-\2.\3"

def change_directory(directory):
    try:
        os.chdir(directory)
        return True
    except OSError as e:
        print(f"Error: <{e.filename}> is not a valid directory.")
        return False

def rename(regular=None, repl=None, test_flag=False):
    flag = False
    for each in os.listdir():
        if not os.path.isfile(each):
            continue

        if re.search(regular, each):
            name = re.sub(regular, repl, each).lower()
            if each == name:
                continue

            flag = True
            if not test_flag:
                shutil.move(each, name)
                print(f">>> <{each}> ---> <{name}>")
            else:
                print(f">>> will rename <{each}> ---> <{name}>")

    if not flag and test_flag:
        print("no file will be renamed")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", help="pattern will used to match the file name")
    parser.add_argument("-r", "--replace", help="replace regular expression")
    parser.add_argument("-d", "--directory", help="directory you want to run the program")
    parser.add_argument("-e", "--execute", help="after debug execute the rename program", action="store_true")
    args = parser.parse_args()

    if args.directory:
    	change_directory(args.directory)

    if args.execute:
        if args.pattern and args.replace:
            rename(regular=args.pattern, repl=args.replace)
        elif not args.pattern and not args.replace:
            rename(regular=AV_PATTERN, repl=AV_REPL)
        else:
            print("pattern and replace must be specified altogether or not")
    else:
        if args.pattern and args.replace:
            rename(regular=args.pattern, repl=args.replace, test_flag=True)
        elif not args.pattern and not args.replace:
            rename(regular=AV_PATTERN, repl=AV_REPL, test_flag=True)
        else:
            print("pattern and replace must be specified altogether or not")

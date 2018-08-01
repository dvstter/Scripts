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
        print(f"Error: <{e.filename}> is not a valid directory.")
        return False

def inner_rename_procedure(origin_name):
    """
    Inner rename procedure, just for japanese av movies
    :param origin_name: original filename
    :return: modified filename
    """
    # let matched filename not to modified
    if re.match(r"^[a-z]{3,}-[0-9]{3,}(-cd\d)?\..*$", origin_name):
        return origin_name

    try:
        # find the contineous characters and numbers set
        characters_set = re.findall(r"[a-zA-Z]{3,}", origin_name)
        numbers_set = re.findall(r"[0-9]{3,}", origin_name)
        # based upon the two sets reconstruct the filename and append with file format
        new_name = characters_set[1] if len(characters_set) > 1 else characters_set[0]
        new_name += numbers_set[1] if len(numbers_set) > 1 else numbers_set[0]
        new_name += "." + origin_name.split(".")[-1]
        return new_name.lower()
    except IndexError:
        return origin_name

def user_defined_rename_procedure(origin_name, regular, repl):
    """
    User-defined rename procedure
    :param origin_name: original filename
    :param regular: match regular expression
    :param repl: replace regular expression
    :return: modified filename
    """
    try:
        if re.search(regular, origin_name):
            new_name = re.sub(regular, repl, origin_name).lower()
            new_name += "." + origin_name.split(".")[-1]
            return new_name
        else:
            return origin_name
    except Exception:
        return origin_name

def rename(regular=None, repl=None, test_flag=False):
    """
    Rename all files name in current directory
    :param regular: user-defined regular expression, must be given altogether with repl
    :param repl: user-defined replace expression, must be given altogether with regular
    :param test_flag: False will execute rename all files, True will only give prompts about how the files will be renamed
    :return: None
    """
    for each in os.listdir():
        # exclude all the directories
        if not os.path.isfile(each):
            continue

        if not regular and not repl:
            # parameters regular and repl are not given, use inner rename procedure
            new_name = inner_rename_procedure(each)
        elif regular and repl:
            # parameters regular and repl are given altogether
            new_name = user_defined_rename_procedure(each, regular, repl)
        else:
            new_name = each

        if each == new_name:
            continue

        if not test_flag:
            # this place can not use os.path.exists, because macosx think
            # lower-case name and higher-case name are same.
            if new_name in os.listdir():
                print(f"Error: file {each} can not be renamed to {new_name}, because the {new_name} existed!")
            else:
                shutil.move(each, new_name)
                print(f">>> <{each}> ---> <{new_name}>")
        else:
            print(f">>> will rename <{each}> ---> <{new_name}>")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", help="pattern will used to match the file name")
    parser.add_argument("-r", "--replace", help="replace regular expression")
    parser.add_argument("-d", "--directory", help="directory you want to run the program")
    parser.add_argument("-e", "--execute", help="after debug execute the rename program", action="store_true", default=False)
    args = parser.parse_args()

    args.execute = not args.execute

    if args.directory:
        change_directory(args.directory)

    if args.pattern and args.replace:
        rename(regular=args.pattern, repl=args.replace, test_flag=args.execute)
    elif not args.pattern and not args.replace:
        rename(test_flag=args.execute)
    else:
        print("Error: pattern and replace must be specified altogether or not")

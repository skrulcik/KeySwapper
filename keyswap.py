#!/opt/local/bin/python

import argparse
import os

ignoredFiles = [ os.path.abspath(__file__) ]

# Implemented as a method so that it can easily be replaced with a more robust
# file-based system later
def retrieveKeys():
    return {
        'PLACEHOLDER1':'ThisIsKey1',
        'PLACEHOLDER2':'ThisIsKey2'
    }

def regularizeDir(dirName):
    if dirName == None or len(dirName) < 1:
        raise ValueError("Directory name cannot be empty")
    if dirName[-1:] == "/":
        return os.path.abspath(dirName) + "/"
    return os.path.abspath(dirName) + "/"

def mapAllFiles(path, mapFun):
    if path == None or len(path) < 1:
        raise ValueError("Path cannot be empty")
    if os.path.isfile(path):
        if os.path.basename(path[0]) != '.' and path not in ignoredFiles:
            mapFun(path)
    elif os.path.isdir(path):
        path = regularizeDir(path)
        for name in os.listdir(path):
            if name[0] != '.':
                mapAllFiles(path + name, mapFun)
    else:
        print("Could not process: " + path)

def replaceInFile(fileName, old, new):
    fd = open(fileName, 'r')
    originalText = fd.read()
    fd.close()
    encodedText = originalText.replace(old, new)
    fd = open(fileName, 'w')
    fd.write(encodedText)
    fd.close()

def replaceInAllFiles(path, old, new):
    replaceAll = lambda f: replaceInFile(f, old, new)
    mapAllFiles(path, replaceAll)

def hideKeys(path, keyDict):
    for placeholder,key in keyDict.items():
        replaceInAllFiles(path, key, placeholder)

def showKeys(path, keyDict):
    for placeholder,key in keyDict.items():
        replaceInAllFiles(path, placeholder, key)

if __name__ == '__main__':
    # Configure command line arguments, at least one must be given
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conceal', action='store_true',
                        help='Conceal keys', default=False)
    parser.add_argument('-r', '--reveal', action='store_true',
                        help='Reveal keys', default=False)
    parser.add_argument('-p', '--path', help='Path to swap keys in',
                        default="./")

    args = parser.parse_args()
    keyDict = retrieveKeys()
    filePath = args.path
    if args.reveal:
        showKeys(filePath, keyDict)
    elif args.conceal:
        hideKeys(filePath, keyDict)
    else:
        parser.print_help()
        print("One of conceal (-c) or reveal (-r) must be given.")


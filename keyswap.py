#!/opt/local/bin/python

import argparse
import os

def regularizeDir(dirName):
    if dirName == None or len(dirName) < 1:
        raise ValueError("Directory name cannot be empty")
    if dirName[-1:] == "/":
        return os.path.abspath(dirName) + "/"
    return os.path.abspath(dirName) + "/"

def retrieveKeys(keydir, ignoredFiles=[]):
    keyDict = {}
    keydir = regularizeDir(keydir)
    for fileName in os.listdir(keydir):
        path = os.path.abspath(keydir + fileName)
        if path not in ignoredFiles:
            fd = open(path, 'r')
            # The name of the file is taken as its placeholder
            # The key is the contents of the file. It is assumed that there is
            # a trailing newline character in the file
            keyDict[os.path.basename(path)] = fd.read()[:-1]
            fd.close()
    return keyDict

def mapAllFiles(path, mapFun, ignoredFiles):
    if path == None or len(path) < 1:
        raise ValueError("Path cannot be empty")
    if os.path.isfile(path):
        if path not in ignoredFiles:
            mapFun(path)
    elif os.path.isdir(path):
        path = regularizeDir(path)
        for name in os.listdir(path):
            if name not in ignoredFiles:
                mapAllFiles(path + name, mapFun, ignoredFiles)
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

def replaceInAllFiles(path, old, new, ignoredFiles):
    replaceAll = lambda f: replaceInFile(f, old, new)
    mapAllFiles(path, replaceAll, ignoredFiles)

def hideKeys(path, keyDict, ignoredFiles):
    for placeholder,key in keyDict.items():
        replaceInAllFiles(path, key, placeholder, ignoredFiles)

def showKeys(path, keyDict, ignoredFiles):
    for placeholder,key in keyDict.items():
        replaceInAllFiles(path, placeholder, key, ignoredFiles)

if __name__ == '__main__':
    # Configure command line arguments, at least one must be given
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conceal', action='store_true', default=False,
                        help='Conceal keys')
    parser.add_argument('-r', '--reveal', action='store_true', default=False,
                        help='Reveal keys')
    parser.add_argument('-p', '--path', default="./",
                        help='Path to swap keys in')
    parser.add_argument('-k', '--keydir', default=".keys/",
                        help="Directory holding key files.")

    args = parser.parse_args()

    # Uses file names and their contents to create a placeholder-key mapping
    keyDict = retrieveKeys(args.keydir)

    # We want to ignore files in the keys directory so they don't get overriden
    # Ignoring . and .. ensures we don't infinitely recurse on directories
    ignoredFiles = [ '.', '..', '.git' ]
    mapAllFiles(args.keydir,
               lambda f: ignoredFiles.append(os.path.abspath(f)),
               ignoredFiles)

    filePath = args.path
    if args.reveal:
        showKeys(filePath, keyDict, ignoredFiles)
    elif args.conceal:
        hideKeys(filePath, keyDict, ignoredFiles)
    else:
        parser.print_help()
        print("One of conceal (-c) or reveal (-r) must be given.")


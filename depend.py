from highlight import *
import subprocess
import os
import time
import pathlib
import shutil
import sys

lilypondPath = "lilypond-2.24.4\\bin"

exePath = sys.executable.split('\\')
exePath.pop()
pythonPath = '\\'.join(exePath)

def sleepExist(fPath):
    while True:
        if os.path.exists(fPath):
            break
        else:
            continue
    

def convertPhys(lyName):
    oemer_cmd = f"oemer {lyName}.png"
    piano_cmd = f"python {pythonPath}\\Scripts\\pianoplayer -o {lyName}.xml {lyName}.musicxml"

    # Run oemer
    subprocess.run(oemer_cmd,shell=True)
    
    sleepExist(f"{lyName}.musicxml")
    subprocess.run(piano_cmd)

def convertXML(lyName):
    convert = f"python {lilypondPath}\\musicxml2ly.py {lyName}.xml"
    convertMidi = f"python {lilypondPath}\\musicxml2ly.py -m -o {lyName}Midi {lyName}.xml"

    sleepExist(f"{lyName}.xml")
    subprocess.run(convert)
    subprocess.run(convertMidi)
    sleepExist(lyName + "Midi.ly")
    subprocess.run(f"lilypond {lyName}Midi.ly")
    


def duplicateFiles(lyName):
    fileTitle = lyName + ".ly"

    measureCount = searchList(readFile(fileTitle))
    p = pathlib.Path('Duplicates')
    for child in p.iterdir():
        os.remove(child)

    for x in range(1,measureCount+1):
        shutil.copyfile(fileTitle,f"Duplicates\\duplicate{x}.ly")

    sleepExist(f"Duplicates\\duplicate{measureCount}.ly")


def generatePNG(lyName):
    fileTitle = lyName + ".ly"
    
    subprocess.run(f"lilypond -fpng --output=measure0 {fileTitle}")

    measureCount = searchList(readFile(fileTitle))
    for x in range(1,measureCount+1):
        os.mkdir(f"PngOutput\\measure{x}")
        highlightMeasure(x,f"Duplicates\\duplicate{x}.ly")
        time.sleep(0.1)
        subprocess.run(f"lilypond -fpng --output=PngOutput\\measure{x} Duplicates\\duplicate{x}.ly")
        

def convert(lyName):
    convertPhys(lyName)
    sleepExist(f"{lyName}.xml")
    convertXML(lyName)
    duplicateFiles(lyName)
    generatePNG(lyName)
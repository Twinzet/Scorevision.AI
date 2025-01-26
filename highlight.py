import os

def renameFile(renamee,ext):
    fName, currExt = os.path.splitext(renamee)
    newName = fName + ext
    os.rename(renamee, newName)
    return newName

def searchList(array):
    i = 1
    while True:
        for l in range(len(array)):
            if array[l].find(f"% {i}") != -1 or array[l].find(f"#{i}") != -1:
                i = i+1
                break
            elif l == len(array)-1:
                return i-1
            


def readFile(fileName):
    lineList = []

    txtName = renameFile(fileName,".txt")

    with open(txtName, 'r') as file:
        lines = file.readlines()
        for row in lines:
            lineList.append(row)

    renameFile(txtName,".ly")

    return lineList

def writeFile(newList, fileName):
        txtName = renameFile(fileName,".txt")

        with open(txtName, "w") as f:
            for line in newList:
                f.write("".join(line))

        renameFile(txtName, ".ly")
    


def checkIfPresent(num, newList, z):

    if num % 10 == 0:
        sym = "#"
    else:
        sym = "% "

    if newList[z].find(f"{sym}{num}") != -1:
        tString = newList[z] ## Extracts content of the current line
        first,second = tString.split(sym)
        
        if int(second) == num:
            return True
    else:
        return False

def measureNotes(startM, fileName, endM="null"):
    if endM == "null":
        endM = startM

    newList = readFile(fileName)
    z = 1
    modList = []

    if startM == 1:
        while z<len(newList):
            if checkIfPresent(1,newList,z) == True:
                modList.append(newList[z])
                modList.append("Break")
            z=z+1
        
    else:
        startM = startM-1
        while z<len(newList):
            if checkIfPresent(startM,newList,z) == True:
                y = z+1
                while checkIfPresent(endM, newList, y) != True:
                    modList.append(newList[y])
                    y = y+1
                modList.append(newList[y])
                modList.append("Break")
            z=z+1
    return modList



def highlightMeasure(measure,fileName):
    newList = readFile(fileName)

    if measure == 1:
        z = 1
        while z<len(newList):
            if newList[z].find("clef") != -1:
                newList.insert(z, f'  \staffHighlight "pink"\n')
                z=z+1

            if checkIfPresent(1,newList,z) == True:
                newList.insert(z+1, f'  \staffHighlight "floralwhite"\n')
                z=z+1
            z=z+1

    else:
        y = 1
        while y < len(newList):
            if checkIfPresent(1,newList,y) == True:
                newList.insert(y, f'  \staffHighlight "floralwhite"\n')
                y=y+1
            y=y+1
        
        startM = measure-1
        endM = measure

        for x in range(startM,endM):
            z = 1
            while z<len(newList)-1:
                if checkIfPresent(x,newList,z) == True:
                    newList.insert(z+1, f'  \staffHighlight "pink"\n')
                    z=z+1

                if checkIfPresent(x+1,newList,z) == True:
                    newList.insert(z+1, f'  \staffHighlight "floralwhite"\n')
                    z=z+1
                z=z+1

    writeFile(newList, fileName)
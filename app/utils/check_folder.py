import os


def checkIfFolderExistsAndCreateIfNot(folderName):

    if not os.path.exists(folderName):
        os.makedirs(folderName)
        return False
    else:
        return True
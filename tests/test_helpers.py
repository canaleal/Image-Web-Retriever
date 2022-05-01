

from app.helpers import checkIfFolderExistsAndCreateIfNot, checkInternetConnection, downloadListOfImagesFromUrl, getListOfPostsThatHaveJPGorPNG

def test_checkIfFolderExistsAndCreateIfNot():
    assert checkIfFolderExistsAndCreateIfNot('app/output') == True
    
def test_checkInternetConnection():
    assert checkInternetConnection() == True

import os
import random, string
from pimThor3.settings import MEDIA_ROOT
from datetime import datetime


def handleUploadFile(file, folderPath, fileName=None):

    if not fileName:
        fileName = file.name
    year, month, day = datetime.now().strftime('%Y %m %d').split()
    folderPath = os.path.join(MEDIA_ROOT, 'UploadFile', folderPath, year, month, day)
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    i = 3
    while fileName in os.listdir(folderPath):
        fileName = "%s_%s" % (''.join(random.sample(string.ascii_letters, i)), fileName)
        i += 1

    filePath = os.path.join(folderPath, fileName)

    with open(filePath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return filePath
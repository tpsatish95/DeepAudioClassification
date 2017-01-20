import os

import eyed3
from eyed3.mp3 import isMp3File


def updateMp3Tags(fileName, mp3genre):
    audiofile = eyed3.load(fileName)
    audiofile.tag.genre = unicode(mp3genre)
    audiofile.tag.save()


if __name__ == '__main__':
    for genre in os.listdir("../data/converted/"):
        if os.path.isdir(os.path.join("../data/converted/", genre)):
            for filename in os.listdir(os.path.join("../data/converted/", genre)):
                mp3FileName = os.path.join("../data/converted/", genre, filename)
                if isMp3File(mp3FileName):
                    updateMp3Tags(mp3FileName, genre)

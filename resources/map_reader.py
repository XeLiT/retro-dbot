import os, io, struct

MAP_DIR = "C:/Users/Ascension/Documents/Coding/BotPixelProject/MapsReader/D2MAPS"

class MapFiles:
    """Create a dictionary as attribute indexes[filePath] =
    {"o":(fileOffset + dataOffset),	"l":fileLength, "stream":f }
    """
    def __init__(self):
        self.indexes = self.getMapsFromD2P()

    def getMapsFromD2P(self):
        ##Go to the right directory
        os.chdir(MAP_DIR)
        files_list = os.listdir(MAP_DIR)
        properties = {}
        indexes = {}

        for file in files_list:
            if os.path.splitext(file)[-1] == ".d2p" :

                ##open D2P file
                f = io.FileIO(file, "r")

                ##read header
                vMax = f.read(1)[0]
                vMin = f.read(1)[0]
                if vMax != 2 or vMin!=1:
                    return None

                ##read parametres at the end of the file
                f.seek(self.getSize(f) - 24)
                unpackedData = struct.unpack("!IIIIII", f.read(24))
                dataOffset = unpackedData[0]
                dataCount = unpackedData[1]
                indexOffset = unpackedData[2]
                indexCount = unpackedData[3]
                propertiesOffset = unpackedData[4]
                propertiesCount = unpackedData[5]

                ##read properties
                f.seek(propertiesOffset)
                i = 0
                while i < propertiesCount :
                    length = struct.unpack("!H",f.read(2))[0]
                    propertyName = f.read(length).decode('utf-8')
                    length = struct.unpack("!H",f.read(2))[0]
                    propertyValue = f.read(length).decode('utf-8')
                    properties[propertyName+file] = propertyValue
                    if propertyName == "link":
                        #we take care of it
                        pass
                    i+=1

                ##read files
                f.seek(indexOffset)
                i = 0
                while i < indexCount :
                    length = struct.unpack('!H', f.read(2))[0]
                    filePath = f.read(length).decode('utf-8')
                    fileOffset = struct.unpack("!I", f.read(4))[0]
                    fileLength = struct.unpack("!I", f.read(4))[0]
                    indexes[filePath] = {"o":(fileOffset + dataOffset),
                                         "l":fileLength,
                                         "stream":f }
                    i+=1

            else:
                pass

        ##Debug
        print("%d maps have just been extracted"%len(indexes))
        #for x in indexes: print(x)

        return indexes

    def getSize(self, fileobject):
        fileobject.seek(0,2) # move the cursor to the end of the file
        size = fileobject.tell()
        return size

class MapInfo(MapFiles):

    def test(self):
        ex1 = self.indexes['3/137253.dlm']
        exMap1 = self.extractData(ex1['o'], ex1['l'], ex1['stream'])

    def extractData(self, o, l, stream):
        ##init vars
        decryptionKey = bytes("649ae451ca33ec53bbcbcc33becf15f4", "utf-8")
        n = len(decryptionKey)
        f = stream
        f.seek(o)

        ##Read header
        header = struct.unpack("!"+"b"*100, f.read(100)) #try to find 77 !
        if 77 in header:
            print("TRUE AT %d"%header.index(77))
        if header == 77:
            mapVersion = f.read(1)[0]
        else:
            print("ERROR")

        ##Debug
        print(header)
        print(f.read(100))

mapFiles = MapInfo()
mapFiles.test()
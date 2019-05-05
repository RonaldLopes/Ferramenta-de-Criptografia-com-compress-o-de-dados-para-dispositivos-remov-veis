from Crypto.Hash import SHA256
import uuid
import pickle
import glob
import os
import zstd
from Crypto.Cipher import AES
import zlib
import hashlib
class EcryptoAdvanced (object):
    def __init__(self,diretorio='./img/*',extesionFilter='', maximumFileSize=(1024*1024*1024)):
        self.directory=diretorio
    def readPath(self):
        filesName= glob.glob(self.directory)
        return filesName
    def readFiles(self): # lê os arquivos
        files=[]
        for name in self.readPath():
            file = open(name,'rb').read()
            files.append({'name':str(name),'file':file})
            file = None
        # print(len(files[1]['file']))
        serializerFiles= pickle.dumps(files) #serializa arquivos

        # print('Tamanho original dos arquivos: '+str(len(serializerFiles)))
        return serializerFiles
    def genL2Key(self, password): # chave de 64 bytes
        l2Key = SHA256.new(password.encode()).hexdigest()
        return l2Key
    def genRamdomKey(self):
        return uuid.uuid4().hex
    def protectCryptoKey(self, password): #criptograda a ramdomKey gerada a partir da Key L2
        pass
    def fibonacci(self,n):
        return n if(n <= 1) else (self.fibonacci(n - 1) + self.fibonacci(n - 2))
    def cryptographyRamdomKey(self,keyL2,ramdomKey):
        # print(keyL2)
        # print(ramdomKey)
        encryption_suite = AES.new(keyL2.encode()[:32], AES.MODE_CFB,keyL2.encode()[:16])
        cryptoFile = encryption_suite.encrypt(ramdomKey.encode())
        return cryptoFile
    def cryptographyFiles(self,files,password):
        encryption_suite = AES.new(password.encode(), AES.MODE_CFB,password.encode()[:16])
        cryptoFile = encryption_suite.encrypt(files)
        return cryptoFile
    def adjustPassword(self,password,size = 32):
        passwordNew = ''
        for i in range(size):
            passwordNew = passwordNew + chr(ord(str(password[i]))+ord(str(password[(i + size)])))
        return passwordNew
    def packetGenerator(self,cryptoFile,cryptoRamdomKey):
        packet = {'packetKey': cryptoRamdomKey,'files':cryptoFile}
        serializerPacket = pickle.dumps(packet)
        compressFile = zstd.compress(serializerPacket, 9)
        return compressFile
    def generateCriptoValidatePacketKey(self,packet,cryptoFile):
        validatePacketKey = self.validatePacketKey(packet)
        # encryption_suite = AES.new(.encode()[:32], AES.MODE_CFB, keyL2.encode()[:16])
        # cryptoFile = encryption_suite.encrypt(ramdomKey.encode())
        # return cryptoFile
    def validatePacketKey(self, packet):
        hash_object = hashlib.md5(packet)
        return hash_object.hexdigest()

    def writeCryptoFile(self, cryptoFiles):
        directory = self.directory.replace('*', '') + 'save.Ecrypto'
        newFile = open(directory, 'wb')
        newFile.write(cryptoFiles)
        newFile.close()
    def feedBackResults(self,files = '',cryptoFile = '',compressFile = '', packetFile = ''):
        print('Tamanho dos arquivos lidos: ' + str(len(files)))  # +' > arquivo: ' + str(files))
        print('Tamanho do arquivo seguro: ' + str(len(cryptoFile)))  # +' > arquivo: ' + str(cryptoFile))
        print('Tamanho do arquivo comprimido ZSTD: ' + str(len(compressFile)))
        print('Tamanho do pacote comprimido: ' + str(len(packetFile)))
    def start(self,password=""):
        ramdomKey = self.genRamdomKey()
        packetKey = self.cryptographyRamdomKey(keyL2=self.adjustPassword(self.genL2Key(password)),ramdomKey=ramdomKey)
        files = self.readFiles()
        compressFile = zstd.compress(files, 9)
        cryptoFile = self.cryptographyFiles(files=compressFile,password=ramdomKey)
        compressFile = None
        packetFinal = self.packetGenerator(cryptoFile,packetKey)
        cryptoFile = None
        # self.feedBackResults(files,cryptoFile,compressFile,packetFinal)
        self.deleteOriginalFiles()
        self.writeCryptoFile(packetFinal)
        packetFinal = None
        print('Criptografia finalizada!')


    ############################### A descriptografia começa aqui ######################################################
    def loadSecureFile(self):
        directory = self.directory.replace('*', '') + 'save.Ecrypto'
        file = open(directory, 'rb').read()
        return file
    def openPacketGenerator(self,packet):
        deCompressfile = zstd.decompress(packet)
        unlockSerializer = pickle.loads(deCompressfile)
        return unlockSerializer['files'],unlockSerializer['packetKey']
    def openCryptoFiles(self, cryptoFiles,cryptoRamdomKey,password):
        ramdomKey = self.decryptRamdomKey(cryptoRamdomKey,password)
        decryption_suite = AES.new(ramdomKey.encode(), AES.MODE_CFB, ramdomKey.encode()[:16])
        files = decryption_suite.decrypt(cryptoFiles)
        return files
    def deleteOriginalFiles(self):
        for name in self.readPath():
            if(name!='') and (name!=None) and (name!=' '):
                comando = 'rm ' +  name.replace(' ','\ ')
                os.system(comando)

    def deleteCryptoFiles(self):
        comando = 'rm ' + self.directory.replace('*','') + 'save.Ecrypto'
        os.system(comando)
    def decryptRamdomKey(self,ramdomKey,password):
        keyL2 = self.adjustPassword(self.genL2Key(password))
        encryption_suite = AES.new(keyL2.encode()[:32], AES.MODE_CFB, keyL2.encode()[:16])
        ramdomKeyUnlock = encryption_suite.decrypt(ramdomKey)
        return ramdomKeyUnlock.decode()
    def writeUnlockFiles(self, serializerFiles):
        block = pickle.loads(serializerFiles)
        for file in block:
            f = open(file['name'],'wb')
            f.write(file['file'])
    def deCryptoStart(self,password = ""):
        finalCryptoFile = self.loadSecureFile()
        compressedCryptoFiles, cryptoRamdomKey = self.openPacketGenerator(finalCryptoFile) #esta certo ate aqui
        files = self.openCryptoFiles(compressedCryptoFiles,cryptoRamdomKey,password)
        decompressCryptoFiles = zstd.decompress(files)
        self.deleteCryptoFiles()
        self.writeUnlockFiles(serializerFiles=decompressCryptoFiles)
# import time
# start = time.time()
# temp = EcryptoAdvanced()
# temp.start('RonaldLopes')
# # temp.deCryptoStart('RonaldLopes')
# end = time. time()
# print(end - start)
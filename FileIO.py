"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###  This class takes care of Write, Read and Append retrieved data from/to file
###  There are 2 types of file classified based on their extensions
###        {fb-user-id}.posts   this file stores all posts excluding comments & reactions
###        {fb-user-id}.txt     this file stores all posts, comments, reactions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class FileIO:
    import os, json  # os is used to retrieve system file path...     # ast
    import hashlib, base64  # used to handle filename one-way encoding
    # Modules installed from http://pycryptodome.readthedocs.io/en/latest/src/installation.html#
    from Crypto.Cipher import AES  # used to handle file encryption and decryption
    from Crypto.Random import get_random_bytes  # this one is used to generate 16 bytes random key
    #SD


    """
        Constructor
        @param filename: list  # remember if we retrieve data from Graph API without any fields,
                                 we got a JSON of userinfo (user name and user id)
                                 put that info here, the function do the rest
        @param onetime_used: bool  # if you only use this FileIO class => pass this
        @param dir: str  # if you want a different dir of your data, set here, if not, it will be the same as this FileIO
    """
    def __init__(self, filename, onetime_used=False, dir=None):
        # If there is no dir defined, the dir will be as same as of this file dir
        if (dir==None): self._dir = self.os.path.dirname(self.os.path.realpath(__file__))
        else: self._dir = dir
        self._fileName = self._encodeFileName(filename)
        self._onetime_used = onetime_used  # see _getPwForEncryptDecrypt or documentation
        self._encryptKey = self._getPwForEncryptDecrypt(filename)
        self._path = self._dir + "\\" + self._fileName
        self._postExt = '.posts'
        self._allDataExt = '.postsNreactz'



    """
        Write the content to file under utf-8 encodings
    """
    def writeToFile(self, data, post = True):
        # Convert to JSON
        data = self.json.dumps(data, ensure_ascii=False)
        # Convert to Bytes because the encryption module only accept bytes value
        data = str(data).encode('utf-8')
        # Prepare the encryption
        print(len(self._encryptKey))
        cipher = self.AES.new(self._encryptKey, self.AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        # Start opening the file and write
        with open(self._getPath(post), 'wb') as file_out:
            try:
                [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
            except IOError:
                print("Could not write to file %s!", self._getPath(post))
                raise

    def readFromFile(self, post = True):
        if (self._fileExist(self._getPath(post))):
            print('Loading data from file %s' % self._getPath(post))

            with open(self._getPath(post), 'rb') as file_in:
                try:
                    # Decrypt the file
                    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
                    cipher = self.AES.new(self._encryptKey, self.AES.MODE_EAX, nonce)
                    data = cipher.decrypt_and_verify(ciphertext, tag)
                    try:
                        return self.json.loads(data)
                    except IOError:
                        print("Could not read the file %s!", self._getPath(post))
                        raise
                except ValueError:  # this is caught by the Encryption module
                    return("Error decryption failed! File was tampered or incorrect key!")
        return "File is not exist"

    def deleteFile(self):
        try:
            if(self._fileExist(self._getPath(True))): self.os.remove(self._getPath(True))  # remove the .posts
            if (self._fileExist(self._getPath(False))): self.os.remove(self._getPath(False))  # remove the .postsNreactz
            print("All your retrieved data have been deleted successful")
        except:
            print("File is not exist or could not be deleted!")

    def getFilePath(self):
        return (self._path)

    def _getPath(self, posts):
        if (posts):
            return (self._path + self._postExt)
        else:
            return (self._path + self._allDataExt)

    def _fileExist(self, path):
        return (self.os.path.exists(path))

    """
        Used in constructor
        To encode the file name that saves the retrieved data
        This will not encode the content of the file
    """
    def _encodeFileName(self, userInfo):
        # Convert data to byte because the hash function require bytes to hash
        name = str(userInfo[0]['name']).encode('utf-8')  # will be the salt
        id = str(userInfo[0]['id']).encode('utf-8')  # will be the pass
        sha2 = self.hashlib.pbkdf2_hmac('sha256', id, name, 100000)  # hash to SHA256, > transfer to hex
        res = self.base64.urlsafe_b64encode(sha2)  # encode the byte result to base64
        return bytes.decode(res)

    def _getPwForEncryptDecrypt(self, userInfo=None):
        if self.isOneTimeUse():
            k = self.get_random_bytes(16)
        else:
            k = userInfo[0]['id'] + userInfo[0]['name']
            k = str(k[:16]).encode('utf-8')  # convert the first 16 characters to bytes
        return k

    def isOneTimeUse(self):
        return self._onetime_used

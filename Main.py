"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###  This class used to have functions that link core functions work
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Main:
    from datetime import datetime
    from FileIO import FileIO
    from Core import Core

    """
        @param token: str  # fb user token
        @param userid: str  # fb user id, used to save the file based on the userid
        @param datadir: str  # place to save the data. As default, the same path of FileIO
                             # format: X:\a\b
    """
    def __init__(self, token, onetime_used=False, datadir=None):
        #Assign token
        self._core = self.Core(token)
        #Get the User ID. This is used to load saved data || OR || save to file
        self._fileio = self.FileIO(self._core.getUser(),onetime_used)
        #self.reactions = self.Reaction()
        #self.translator = Language('ja')

    """
        Use this function to retrieve data for the first time ever
        or just to get the latest data
        @param type: str  # posts, comments, reactions - type of data to get, can get separately
        @param posts: bool  # True if this is the Parent data (data to get post id)
                            # False if this is the Child sub-data (have different file IO ext)
        @param getAll: bool  # True, save all data (comments, reactions) in the same file
                             # Indeed, the posts also be there
    """

    def _retrieveData(self, type='posts', posts=True, getAll=False):
        # 0 count the time for reference
        start = self.datetime.now()
        # 1 Start
        # Actually, we can have 2 types of data to retrieve
        #   1. the parent data, from this, we have id to access other comments and reactions
        #   2. the child data, which are COMMENTS and REACTIONS at this moment
        # I make the if/else like this to give a further scalable version,
        # but we still can combine two jobs (comments and reactions) as together.
        if type == 'posts':
            # Load all posts first, no comments and reactions
            data = self._core.getPosts()
        elif type == 'comments':
            # Comments would loaded based on post id inside the POSTs
            # core.getComments has 1 param of posts data. Hence, load all posts first and put here
            # loadPostsData only used to get the Parent posts, used if extract the Reactions alone
            data = self._core.getComments(self.loadPostsData())
        else:
            # Reactions, same as Comments
            if(getAll):
                # Different here is
                # We ordered the reactions to be extracted at last
                # So, it could be extracted a lone, or with the Comments
                # Everytime the sub data is extracted, they will be saved
                # The Comments are save before this Reactions
                # Therefore, if get all data, this function must open the last file, which includes Comments
                data = self._core.getReactions(self.loadAllData())
            else:
                # loadPostsData only used to get the Parent posts, used if extract the Reactions alone
                data = self._core.getReactions(self.loadPostsData())
        # 2 Save

        if (data != []):
            try:
                self._fileio.writeToFile(data, posts)
                print('Data were saved successful!\n')
                result = True
            except:
                print('FileIO error!')
                result = False
        else:
            print('No data were saved!')
            result = False
        # 3 Print status
        end = self.datetime.now()
        runtime = end - start
        print("Done after %s ms\n" % (str(runtime.seconds * 100)))
        return (result)

    def retrievePosts(self):
        print('Start to retrieve all Posts...')
        return self._retrieveData('posts')

    def retrieveComments(self):
        print('Start to retrieve all Comments...')
        return self._retrieveData('comments', False)  # False => include comments // reactions => saved under different extension

    def retrieveReactions(self, getAll=False):
        print('Start to retrieve all Reactions...')
        return self._retrieveData('reactions', False, getAll)


    """
        This is one of the first Functions ever you have to run to get all data you need
        This function will retrieve all information in order as Posts // Comments // Reactions
        Each one would be saved once before the next one
        Only a success privious one allows the continue of the next one
        Return TRUE if successful, otherwise, FALSE
        
        Alternatives: I have not implement a way to keep track of what already saved, if one of the step wrong, its wrong
                      So, the alternative way, not need to change the code, is to perform separatetly the retrieve data
                      There are 3 functions above, run it separately
                      Because the Posts would be saved in a separate file,, this is important not to cost much of time
                      Do the retrievePosts before any other else
    """

    def retrieveAllData(self):
        # 0 count the time for reference
        start = self.datetime.now()
        if(self.retrievePosts()):  # Retrieve Posts and ONLY when success --> go next
            if(self.retrieveComments()):  # Retrieve Comments and ONLY when succeed --> go next
                if(self.retrieveReactions(True)):  # Retrieve Reactions
                    result = True  # Result to return
                else:
                    result = False
            else:
                result = False
        else:
            result = False
        print("\nFinished retrieving all data including posts, comments, and reactions!")
        # 3 Print status
        end = self.datetime.now()
        runtime = end - start
        print("Done everything after %s ms" % (str(runtime.seconds * 100)))
        return(result)

    # This is used for private, receive the POSTS data only (for further processing)
    # From this data, the program will get id and from that, the comments and reactions
    def loadPostsData(self, filename=None):
        return (self._fileio.readFromFile())

    # This is used for public retrieve
    # Then, the data retrieved here will include all posts, their comments and reactions
    def loadAllData(self, filename=None):
        return (self._fileio.readFromFile(False))

    """
        This will delete the data if onetime_used (see __init__ or fileio) TRUE
    """
    def endSession(self):
        if (self._fileio.isOneTimeUse()):
            self._fileio.deleteFiles()


    def printAllData(self):
        print(self.loadAllData())

    def totalPosts(self): # not test
        return len(self.loadAllData()['data'])

    ### FROM HERE - FOR TESTING PERPOSE ONLY ###
    def getUserInfo(self):
        return self._core.getUser()

    def write(self, data):
        self._fileio.writeToFile(data)
    def read(self):
        return(self._fileio.readFromFile())


    """def countReactions(self): # not test
        self.reactions.appendReaction(self.loadAllData())
        print(self.reactions.reactionLists())"""
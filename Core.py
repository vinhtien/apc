# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 15:00:32 2017

@author: Elnur, Tien
"""

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###  This class contains main methods to retrieve and process data directly from FB
###  To retrieve data from FB (post, comment,...) of a person in JSON
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Core:

    import urllib.request
    import urllib.error as error
    import json, time


    """
        Construction
        @param: token # unique token generated by FB under the user authentication
        @param: mainURL # the main URL to access all related information based parameters in a profile
        @param: profileURL # start by 'me?' => return name and id of user
        @param: postURL # start by profileURL + 'fields=posts'
        """

    def __init__(self, token):
        self._token = token
        self._accessToken = '&access_token=' + self._token
        self._apiversion = 'v2.11/'
        self._mainURL = 'https://graph.facebook.com/' + self._apiversion
        self._timeOut = 1  # (seconds) used to wait in between URL retrieving:: MIN 18s/retrieve/account
        self._networkTimeOut = 10  # (seconds) used to wait inside the __getJSON if there is an error
        self._numberOfRetries = 6  # used to define the number of retries of fail __getJSON
        self._getDataError = ""  # used to record errors
        self._totalRetrieve = None  # Batch counter: used to record batch of sub data retrieval time. NONE means not activated
                                   # this will be activated when sub data are retrieved
        self._retrieveCount = 1  # used to count every data retrieval time in a batch of data
        self.totalRequests = 0  # used to count total requests made by this class from Instance
        self._urlShow = True  # True to use in case of Debug. Can be set to False, no URL will be printed
        self._batchSize = 100  # number of posts retrieved in a single API call (FYI: FB's default is 25)


    """
        prepareURL
        @userinfo = False # True: retrieve user name and id
        @posts = False # True: retrieve all posts of a user
        @subPostId = '' # only assign value if retrieve content of a specific post
                        if userinfo = TRUE => subPostId would not work
            @commentsOfPost = False # True: retrieve comments in the post
            @reactionsOfPost = False # True: retrieve reactions in the post
    """

    def _prepareURL(self, userinfo=False, posts=False, subPostId = '', commentsOfPost=False, reactionsOfPost=False, allConnections = False):
        # DEFAULT, Only receive the userid and user name
        fields = 'me?fields=id,name'
        if (userinfo):
            fields = 'me?fields='
            # if receive all posts
            fields += self._getFields(posts, subPostId, commentsOfPost, reactionsOfPost, allConnections)
        else:
            fields = self._getFields(posts, subPostId, commentsOfPost, reactionsOfPost, allConnections)
        return self._mainURL + fields + self._accessToken


    """
        The lowest level of function to request JSON from FB. There also a retry control
        based on __networkTimeOut and __numberOfRetries 
        :param field: str  # the field of data to retrieve
        :param url: str  # the main URL to retrieve data
        return JSON
    """

    def _getJSON(self, url):
        retriedCount = 0
        while retriedCount < self._numberOfRetries:
            # First, put a Request command
            self.totalRequests += 1
            reg = self.urllib.request.Request(url)
            try:
                print('.request (%s) page (%s) retrieving from: %s' % (self.totalRequests, self._retrieveCount, url if (self._urlShow) else 'Facebook'))
                response = self.urllib.request.urlopen(reg)
                try:
                    data = self.json.loads(response.read(), encoding='UTF-8')
                    # taking a short snap
                    self.time.sleep(self._timeOut)
                    self._retrieveCount += 1
                except ValueError as ve:
                   self._dumpError(str(ve))
            except self.error.HTTPError as httpe:
                self._dumpError(httpe, 'http')
            except self.error.URLError as urle:
                self._dumpError(urle, 'url')
            # Check for error to determine a retry or not
            if (self._checkError()):
                retriedCount += 1
                print("retrying (%s) after %ss..." % (retriedCount, self._networkTimeOut))
                self.time.sleep(self._networkTimeOut)
            else:
                break
        # if there is error, variable data would not be defined => check first
        if 'data' in locals(): return (data)
        return None


    """
        This function retrieve data directly from the Facebook
        data is retrieved in every specific entity (a user, a post, a comment)
        We can simplify those parameters quite easily as just 3 parameters [posts(T/F), postID, comments(T/F)].
        However, I put it like this so we can understand easier and more clearly
        in our group and also easy for further scalability, if needed.
        As the time flies, those parameters could be reduced
        
        @param userinfo: bool  # True: receive the user info only, nothing else!!!
        @param posts: bool  # True: receive all the posts of a profile, nothing else!!!
        @param subPostId: str  # If not empty, receive Comments or Reactions
            @param commentsOfPost: bool  # True, receive Comments, nothing else!!!
            @param reactionsOfPost: bool  # True, receive Reactions, nothing else!!!
    """

    def _getData(self, userinfo=False, posts=False, subPostId='', commentsOfPost=False, reactionsOfPost=False, allConnetions = False):
        # 1::  prepare a URL that includes all necessary parameters for data retrieval
        parentURL = self._prepareURL(userinfo, posts, subPostId, commentsOfPost, reactionsOfPost)
        # 2::  Because the data will be return in JSON with levels of keywords, this to know which level we should get the info from
        field = self._getFields(posts, subPostId, commentsOfPost, reactionsOfPost, allConnetions)
        # COUNTER and START MESSAGE
        self._getDataCounter()
        # 3::  Start to get the JSON - This will get the FIRST PAGE and put into a list-type data variable
        data = [self._getJSON(parentURL)]

        # 4::  Get the next page from the FIRST PAGE
        nextURL = self._getNextURL(field, data)

        # 5::  Continue to get SECOND PAGE, and so on... if any
        while (nextURL != None and data != None):
            newData = self._getJSON(nextURL)
            if(newData == None): break  # There is error, exit loop
            # append to the previous data
            data[0][field]['data'].extend([newData][0]['data'])
            # get the next URL from the retrieved data
            nextURL = self._getNextURL(field, newData)  # get another Next URL

        # 6: return the data
        if (self._checkError()):  # if there is ERROR, this function will print and return True
            return None  # return None <=> error
        try:  # data is not empty, return the lowest meaningful level of content
            return (data[0][field]['data'])
        except: # data is empty, return empty list
            return []


    """
        Used to handle counter for data and sub-data retrieving
    """

    def _getDataCounter(self):
        if (self._totalRetrieve != None):
            self._totalRetrieve += 1  # count for all parent page
            print('Batch (%s)' % str(self._totalRetrieve))
        self._retrieveCount = 1  # count for all child page of the parent


    """
        Every post has it post id. Based on this id, function will get data of comments or reactions using that post id
        In fact, each post id can have 1 or many comments or reactions
        Therefore, this function is used to run a loop to traverse every post id and get all comments or reactions of that
        In every loop, function will call __getData
        This call will return the data of comments of reactions or whatever a sub level items (scalable)
    """

    def _getSubData(self, posts, commentsOfPost=False, reactionsOfPost=False):
        # Activate the Batch counter
        self._totalRetrieve = 0  # count for all pages
        # Which type of data ? - Can be scalable
        type = 'comments' if commentsOfPost else 'reactions'
        try:
            for id in posts:
                id[type] = self._getData(False, False, id['id'], commentsOfPost, reactionsOfPost)
            return posts
        except Exception:
            return None


    """
        This is used to extract the post id from a list of POSTS that had been retrieved
        """
    def _getPostIds(self, data):
        return [ x['id'] for x in data]


    """
        This is used to recognize which fields will be in the JSON before retrieve the data
        """

    def _getFields(self, posts=False, subPostId='', commentsOfPost=False, reactionsOfPost=False, allConnections=False):
        if (posts):
            field = 'posts'  # If the retrieve data are POSTS, Otherwise...
            if allConnections:
                field += '{comments{reactions,comments{reactions}},reactions}'  # If all comments and reactions are requested
            return field
        elif (subPostId != ''):  # If there is subPostId input, will receive comment or reaction
            # Then, the field could only be Comments || OR/AND || Reactions
            field = subPostId + '?fields='
            if (commentsOfPost and reactionsOfPost):
                field = 'comments,reactions'
                return field
            elif (commentsOfPost):
                field = 'comments'
                return field
            elif (reactionsOfPost):
                field = 'reactions'
                return field
        return ''


    """ getNextURL
        return the Next URL in the paging value of the JSON data result
        """

    def _getNextURL(self, field, data):
        import re
        try:
            # This case happens when this is the FIRST PAGE
            result = data[0][field]['paging']['next']
        except:
            try:
                result = data[field]['paging']['next']
                # This case happens when this is the NEXT PAGE
            except:
                try:
                    result = data[0]['paging']['next']
                except:
                    try:
                        result = data['paging']['next']
                    except:
                        # There is no NEXT PAGE
                        return None
        result = re.search(r'(.+limit=)(\d+)(.+)', result)
        result = result.group(1) + str(self._batchSize) + result.group(3)  # Insert our own batchsize
        return result


    """
        Used to save the Error returned when Try to retrieve JSON data from Facebook
        @param: errObject # object: the error object of URLError or HTTPError in exception
        @param: type # str: http if httperror || OR || url if urlerror related
        @param: value # str: in case just the error value

    """

    def _dumpError(self, errObject = None, type = '', value = ''):
        if (errObject != None):
            if (type == 'http'):  # Error relating to HTTP
                self._getDataError += "The server couldn\'t fulfill the request.\n"
                self._getDataError += ("Error code: " + str(errObject.code))
            elif (type == 'url'):  # Error relating to URL
                self._getDataError += "We failed to reach a server\n"
                self._getDataError += ("Reason: " + str(errObject.reason))
        else:
            self._getDataError += value


    """
        This private method is used to check if there is error saved in the object and printout
    """

    def _checkError(self):
        if (self._getDataError != ""):
            print('!---- ERROR ----!\n%s\n' % (self._getDataError))
            self._getDataError = ""  # reset to empty
            return True
        else:
            return False


    def getUser(self):
        url = self._prepareURL(userinfo=True)
        result = [self._getJSON(url)]
        print('User info is retrieved successful!')
        return result

    def printUser(self):
        print(self.getUser())

    def getPosts(self):
         return(self._getData(True, True))

    def printPosts(self):
        print(self.getPosts())

    def getComments(self, posts):
        return(self._getSubData(posts, True))
        #return(self._getData(False, False, posts, True))

    def printComments(self, posts):
        print(self.getComments(posts))

    def getReactions(self, posts):
        return (self._getSubData(posts, False, True))
        # return(self._getData(False, False, posts, False, True))

    def printReactions(self, posts):
        print(self.getReactions(posts))

    def setBatchSize(self, size):
        #  Sets size of request (number of posts retrieved in a single API call)
        self._batchSize = size

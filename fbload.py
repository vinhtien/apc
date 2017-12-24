import json
import requests as req
import re
import time


class FBLoad:

    def __init__(self, newtoken):
        self._token = newtoken
        self._posts = self.initfeed(self, newtoken)

    def initfeed(self, tkn):
        postreq = "https://graph.facebook.com/v2.11/me?fields=posts&access_token=" + tkn
        initPost = req.request('GET', postreq)
        posts = [initPost.json()]
        return posts

    def loadfeed(self):

        nextpage = self._posts[0]['posts']['paging']['next']  # link to next batch

        def getnextpost(nextpage):  # recursively get all posts in batches of 25
            nextrequest = re.search(r'(.+limit=)(\d+)(.+)', nextpage)
            try:
                nextrequest = nextrequest.group(1) + "25" + nextrequest.group(3)
            except TypeError:
                nextrequest = nextpage
            response = req.request('GET', nextrequest)
            response = response.json()  # its a dict, same as usual
            self._posts.append(response)
            print("Posts loaded:" + str(len(self._posts)))
            nextpage = self._posts[-1]['paging']['next']
            getnextpost(nextpage)

        try:
            getnextpost(nextpage)
            print(len(self._posts) + " posts loaded")
        except:
            pass  # Run until an error is raised at end of feed



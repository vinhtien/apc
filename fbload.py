import json
import requests as req
import re
import time

token = 'EAACEdEose0cBAJAuIzcBLlv9aexa7Yt6oxcy6fkYhYG3ZBWNvsxfBA5CCtAviuc20ixksdtrGTffFjhvQqC6OSZBa5ZAAl71LT75jZCsOjnrGrQIJtnMqaCZCaUjliYZCHyjh3lTPgg32TZAnoXWOVdNlQSS26CdyvVZCMxZAd5zwlkALfEE6sLSPa3eBAsXUAgsZD'
myid = "843413639079453"
# get the first batch of posts, as it contains link to the next batch
postreq = "https://graph.facebook.com/v2.11/me?fields=posts&access_token=EAACEdEose0cBAJAqgEgNkYIkzf4ZBSx5Ch6iMoYWqeoORk3mNefuDechV46vAioIj02S6SWxvW3c7GzBK3jbBhKVZA4poH06Y2ZBZAPvXr6Jjcvke82WKMcyi76PWOOvIWgheKs2ioZB9gSgTilFQtWAFsPBSJEUDU1588wXJZCmJ5BpYkO9ZAZAUfZBcBqmfdnwZD"
match = re.match(r'(.+token=)(\w+)', postreq)
postreq = match.group(1) + token
posts = req.request("GET", postreq)
posts = [posts.json()]
session = req.Session()
nextpage = posts[0]['posts']['paging']['next']  # link to next batch


def getNextPost(nextpage):  # recursively get all posts in batches of 25
    nextrequest = re.search(r'(.+limit=)(\d+)(.+)', nextpage)
    try:
        nextrequest = nextrequest.group(1) + "25" + nextrequest.group(3)
    except TypeError:
        nextrequest = nextpage
    response = session.request('GET', nextrequest)
    response = response.json()  # its a dict, same as usual
    posts.append(response)
    print("Posts loaded:" + str(len(posts)))
    nextpage = posts[-1]['paging']['next']
    getNextPost(nextpage)


try:
    getNextPost(nextpage)
    print(len(posts) + " posts loaded")
except:
    pass

count = 0
db = []
posts[0] = posts[0]["posts"]
for piece in posts:
    for apost in piece['data']:
        db.append(apost)
print(len(db))
del posts


def getReactz(postid):
    #  sample GET request of comments and reactions
    test = 'https://graph.facebook.com/v2.11/843413639079453_1555983771155766?fields=comments%2Creactions&access_token=EAACEdEose0cBALRkRJRY4LCVnJbWNKAPeTpyhVg8CTjWHRBvKnJhVsQx85X4ZCTNAZASQrqD9TPGcLkHSAuaSu0OdnNHHrTi3F5ntYFrG2SgDiRh95o23NFRpecZBY2JpjO4lRmZAkqcDmi1lqKpuDJIZCKdTaWnOGOUaFt9j0DZBsnlALrpxwEft3EJcq7FwZD'
    match = re.search(r'(.+v2.11\/)(\w+)(\?fields.+access_token=)(\w+)', test)
    validrequest = match.group(1) + str(postid) + match.group(3) + token
    #  replace old token. group No2 is post ID
    output = req.request("GET", validrequest, timeout=60)  # timeout is in seconds
    #  ['comments'] and ['reactions'] both follow this structure: [u'paging', u'data']
    return output.json()


startime = time.time()
apicounter = 0
output = []
try:
    with open('postsNreactz.txt', 'r') as file:
        output = json.load(file)
except FileNotFoundError:
    with open('postsNreactz.txt', 'w') as file:
        print('created new file')
        fileisemtpy = True
except json.decoder.JSONDecodeError:
    pass
waitforapi = False
for i in range(len(output), len(db)):

    with open('postsNreactz.txt', 'r') as file:
        try:
            output = json.load(file)
        except json.decoder.JSONDecodeError:
            pass

    if waitforapi:  # there is a limit on api calls
        print("Sleeping for API call limit: " + str(300) + 's')
        with open('postsNreactz.txt', 'w') as file:  # backup the data!
            json.dump(output, file)
            print('data saved!')
        time.sleep(300)
        startime = time.time()

    print(str(i) + ' is running \n')
    try:
        postid = output[i]['id']
    except IndexError:
        postid = db[0]['id']
    try:
        reactz = getReactz(postid)
    except:
        waitforapi = True
        print("API wait is triggered!")
        continue
    apicounter += 1
    output.append(db[i])  # copy current post into output
    try:  # adding reactions if they exist
        output[i]['reactions'] = reactz['reactions']['data']
    except KeyError:  # in case there are no reactions
        output[i]['reactions'] = []
        pass
    try:  # add comments if they exist
        output[i]['comments'] = reactz['comments']['data']
    except KeyError:  # there are no comments so it does not exist
        output[i]['comments'] = []
        pass
    with open('postsNreactz.txt', 'w') as file:
        json.dump(output, file)
        print('data saved!')
    print ('post no.' + str(i))
    continue

with open('postsNreactz.txt', 'w') as file:  #save again for a good measure))
    json.dump(output, file)
    print('data saved!')



from Main import Main
import json
import hashlib, binascii,base64

#XcYEgogQX0MobP1mOEjaNNtPh6Qe0ONB0JhBFwhW-Fc=

__userToken = 'EAACEdEose0cBAILZCwVDJdPFUqhluPruxc7YXVwAWMFgIpemdqnKEZBCdNQmMfJxKSt92A2o0SWVCfBvkZC7j8NoDkOglZA41hUfKsiVLEKfSJfts8G3WgdVBWl13E0D5FZChq8IXyK6Op2Dy0sUSUcZBlejEZBilGfNOaHApUUJdZCKdKbJzzeNngIoMUag61gZD'
#__userID = '545838748863640'
__onetime_used = False
__dataPath = 'D:\STUDY\MSCCOMPSCI\Proj_APC17\spa'
# if dataPath = NONE => it's fine, FileIO will use the same path of it
m = Main(__userToken, __onetime_used, __dataPath)
#m.retrieveAllData()


############### USE THIS - TRY THIS - TEST THIS ####################
#PLAY WITH THE MAIN :)

### RETRIEVE DATA FROM FB
#OPTION 1 (MUST DO 2 PHASE, ONE-BY-ONE
#PHASE 1:: retrieve the POSTS
#m.retrievePosts()
#PHASE 2::
#m.retrieveComments()
#m.retrieveReactions()

#OPTION 2
#m.retrieveAllData()


### LOAD DATA FROM FILE SYSTEM
#data = m.loadAllData()
#print(data)
#return data
####################################################################












"""file = open('postsNreactz.txt','r')
output = json.loads(file.read())
print(type(output))
#print(output)
print([i.get('message') for i in output])"""


#print([i.get('comments') for i in d])

#m.retrieveComments()
#d = '{"data":[{"created_time":"2013-12-15T09:01:16+0000","from":{"name":"Steven Nguyen","id":"1507685362678969"},"message":"m\u00e0y nh\u00ecu chi\u1ec7n \u0111\u00f3 :3","id":"486290441485138_2505995"},{"created_time":"2013-12-15T09:01:44+0000","from":{"name":"N\u1edd T\u1edd","id":"1517041091677769"},"message":"thag nao cug giong thang nay ha!!!kaka","id":"486290441485138_2505997"},{"created_time":"2013-12-15T09:02:05+0000","from":{"name":"Thuat Nguyen","id":"1543267142427312"},"message":"moa ! que nhe ! ghet, t unf m luon, mai mot co add t lai t ko co accept dau nha kon","id":"486290441485138_2505998"},{"created_time":"2013-12-15T09:06:07+0000","from":{"name":"Steven Nguyen","id":"1507685362678969"},"message":":3","id":"486290441485138_2506004"},{"created_time":"2013-12-15T17:48:58+0000","from":{"name":"L\u00ea Ho\u00e0ng Ph\u01b0\u01a1ng","id":"1990103811005932"},"message":"\u0e0f\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e\u0e4e(\u25d4 \u0434\u25d4) \u0e04\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49\u0e49","id":"486290441485138_2507010"},{"created_time":"2013-12-16T04:05:42+0000","from":{"name":"Steven Nguyen","id":"1507685362678969"},"message":"m\u00e0y bi\u1ec3u \u0111\u1ea1t c\u00e1i g\u00ec v\u1eady L\u00ea Ho\u00e0ng Ph\u01b0\u01a1ng","id":"486290441485138_2507951"},{"created_time":"2013-12-16T04:14:50+0000","from":{"name":"Thuat Nguyen","id":"1543267142427312"},"message":"ngon ngu meo chang?","id":"486290441485138_2507967"},{"created_time":"2013-12-16T04:49:30+0000","from":{"name":"Phoebe Truong","id":"1526385930783632"},"message":"No\u0301 k\u00eau \"meo meo\" \u0111o\u0301.","id":"486290441485138_2508012"},{"created_time":"2013-12-16T04:59:48+0000","from":{"name":"T\u1ea1 Xu\u00e2n Duy","id":"915948538573496"},"message":"hi\u1ec3u ti\u1ebfng m\u00e8o lu\u00f4n","id":"486290441485138_2508020"}],"paging":{"cursors":{"before":"WTI5dGJXVnVkRjlqZAFhKemIzSTZAORGcyTXpJd05EazRNVFE0TnprNU9qSTFNRFU1T1RVPQZDZD","after":"WTI5dGJXVnVkRjlqZAFhKemIzSTZAORGcyTnpNeE1qY3hORFF4TURVMU9qSTFNRGd3TWpBPQZDZD"},"previous":"https:\/\/graph.facebook.com\/v2.11\/1507685362678969_486290441485138\/comments?access_token=EAABZCTyXOsswBAKRaPOoqR1VAaoUtRkwk1dtRjZCGzEHZASnwgzSVWsImKpt8WKlUsLzxtCYG51ISnqVRcGTQaZCKDUY0pIF15jZAFKkruavC1rKstKZABwT7czlYbOk0KwHFn3RHeAGKRZAZCm1pYnQZAFpZBQZB1zWz7EdebsQdWfr4UpFE5l8KinANO5kvrBEBMZD&limit=25&before=WTI5dGJXVnVkRjlqZAFhKemIzSTZAORGcyTXpJd05EazRNVFE0TnprNU9qSTFNRFU1T1RVPQZDZD"}}'
#print(d[1])
#PHASE 2:: retrieve the COMMENTS and REACTIONS
#m.retrievePosts()


#d = {}
"""file = open('545838748863640.posts','r',  encoding="utf-8")
output = json.loads(file.read())
print(type(output))
#d = m.loadPostsData()
print(len(output))
#for i in range(0, len(output)):
 #   print(output[i]['id'])

print([i.get('message') for i in output])
#print(d[0]['id'])
#d = [ x['id'] for x in d]
#print(d)
#print(d[0]['id'])
#d[0]['reactions'] = d[1]
#print(d[0])
#print(d[0]['reactions']['story'])
#for i in d:
    #print(i.append('comments'))

#print(len(d))
#print(d)
#m.printData()
#print(m.totalPosts())
#m.countReactions()"""
"""
with open("D:\STUDY\MSCCOMPSCI\Proj_APC17\spa\XcYEgogQX0MobP1mOEjaNNtPh6Qe0ONB0JhBFwhW-Fc= - Copy.postsNreactz", 'r', encoding="utf-8") as file_in:
    a=(json.load(file_in))
    #print(type (a))
    print(a)
    #m.write(a)

a = m.read()
print(a)
print(type(a))

"""
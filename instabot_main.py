import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt
import collections

Access_Token = "3540677334.55d5542.dc3f76bc01674c5796e4eba7d4c142c0"
base_url = "https://api.instagram.com/v1/"


def self_info():
    '''
    1.create a url for self account
    2.request the data
    '''
    request_url = (base_url + "users/self/?access_token=%s")%(Access_Token)
    print 'My requested URL is :- %s'%(request_url)
    user_info = requests.get(request_url).json()

    print user_info

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print "Username is :- %s" %(user_info['data']['username'])
            print "Number of Followers :- %s" %(user_info['data']['counts']['follows'])
            print "Number of Peoples Followed by you :- %s"%(user_info['data']['counts']['followed_by'])
            print "Number of Posts :- %s" %(user_info['data']['counts']['media'])
        else:
            print "User Doesn't Exist !"
    else:
        print "Invalid Information !"
    return user_info


def get_user_id(user_name):

    request_url = (base_url + "users/search?q=%s&access_token=%s") % (user_name,Access_Token)
    print "The requested URL is :- %s"%(request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code']==200:
        if len(user_info):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print "The User Doesn't Exist "
        exit()


def get_user_info(user_name):

    user_id = get_user_id(user_name)
    if user_id==None:
        print "User Doesn't Exist"
        exit()
    requested_url = (base_url + "users/%s/?access_token=%s")%(user_id,Access_Token)
    user_info = requests.get(requested_url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print 'UserName is :- %s'%(user_info['data']['username'])
            print 'Number of Followers :- %s'%(user_info['data']['counts']['followed_by'])
            print 'Number of People Following :- %s'%(user_info['data']['counts']['follows'])
            print 'Number Of Posts :- %s'%(user_info['data']['counts']['media'])
        else:
            print 'NO DATA FOUND!!'
    else:
        print "User Doesn't Exists"

def get_own_post():

    '''
    1.we need a access token and base url
    2.generate url
    3.generate recent post
    '''

    requested_url = base_url + "users/self/media/recent/?access_token=%s" %Access_Token
    my_recent_post = requests.get(requested_url).json()['data'][0]['id']
    print my_recent_post
    return my_recent_post


def dowmload_post(item):

    urllib.urlretrieve(item['url'] , item['image_name'])
    return None

def download_own_posts():

    '''
    1.get the user info
    2.create url and name
    3.call download post
    '''

    requested_url = base_url + "users/self/media/recent/?access_token=%s" %Access_Token
    data = requests.get(requested_url).json()['data']
    images = []
    for e in data :
        images.append({'url' : e['images']['standard_resolution']['url'],
                       'image_name': e['id'] + '.jpeg'})
    for e in images :
        dowmload_post(e)
    print "Your Posts are Ready"

def get_another_user_recent_post(user_name):

    '''
    1.search the user
    1.generate userid from search
    3.get the most recent media of the user by using endpoint
    '''

    user_id = get_user_id(user_name)
    requested_url = base_url + "users/%s/media/recent/?access_token=%s" %(user_id,Access_Token)
    posts = requests.get(requested_url).json()['data']
    images = []
    for e in posts:
        images.append({'url': e['images']['standard_resolution']['url'],
                       'image_name': e['id'] + '.jpeg'})
    for e in images:
        dowmload_post(e)
    print "Your Images Are Ready ^_^\n"
    exit()

def get_post_id(user_name):

    '''
    1.fetch the user_id
     2.create request_url
     3.fetch recent media id
    '''

    user_id = get_user_id(user_name)
    requested_url = base_url + "users/%s/media/recent/?access_token=%s" %(user_id,Access_Token)
    media_id = requests.get(requested_url).json()['data'][2]['id']
    return  media_id

def like_a_post(user_name):

    '''
    1.get post id with get_post_id() function
    2.generate request url
    3.create parameter payload
    4.post like
    '''

    post_id = get_post_id(user_name)
    print post_id
    request_url = (base_url + 'media/%s/likes')%(post_id)
    payload = {'access_token': Access_Token}
    print "Post request URL :- %s" %request_url
    post_a_like = requests.post(request_url,payload)
    if post_a_like.json()['meta']['code'] == 200 :
        print "You Posted a Like"
        exit()
    else :
        print "Like Was Unsuccessful"
    return  post_a_like

def post_a_comment():

    '''
    1.create post id
    2.create request url
    3.create parameter with access token and text
    4.call the function
    '''

    post_id = get_own_post()
    request_url = base_url + "media/%s/comments"%(post_id)
    param ={'access_token':Access_Token , 'text':'api comment testing'}
    post_comment = requests.post(request_url,param)
    print "You Posted a Comment"
    return post_comment

def get_comment(user_name):

    '''
    1.fetch post_id with function get_post_id
    2.create request_url
    3.fetch the comments
    '''

    post_id = get_post_id(user_name)
    request_url = base_url + 'media/%s/comments?access_token=%s' %(post_id,Access_Token)
    print request_url
    data = requests.get(request_url).json()['data']
    comments = []
    for e in data:
        comments.append(e['text'])
    print "\n" , comments
    return comments




def media_liked_by_user():

    '''
    1.create request url
    2.fetch the information
    '''

    request_url = base_url + "users/self/media/liked?access_token=%s"%(Access_Token)
    liked_media = requests.get(request_url).json()['data'][0]['caption']
    print liked_media
    return liked_media


def tag_object_information(tag_name):

    '''
    1.choose a tag
    2.create the url
    3.fetch the information
    '''

    request_url = base_url + "tags/%s?access_token=%s" %(tag_name,Access_Token)
    information = requests.get(request_url).json()['data']
    print information
    return information

def recent_tagged_media(tag_name):

    '''
    1.pass a tag_name
    2.create url
    3.fetch information
    '''

    request_url = base_url + "tags/%s/media/recent?access_token=%s" %(tag_name , Access_Token)
    media = requests.get(request_url).json()['data']
    print media
    return media

def search_tag_by_name(tag_name):

    '''
    1.pass a query tag without #
    2.create url
    3.fetch the information
    '''

    request_url = base_url + "tags/search?q=%s&access_token=%s" %(tag_name , Access_Token)
    tag_info = requests.get(request_url).json()['data']
    print tag_info
    return  tag_info


def get_comment_for_delete_function(user_name):

    '''
    1.fetch post_id with function get_post_id
    2.create request_url
    3.fetch the comments
    '''

    post_id = get_post_id(user_name)
    request_url = base_url + 'media/%s/comments?access_token=%s' %(post_id,Access_Token)
    data = requests.get(request_url).json()
    return data


def delete_negative_comment(user_name):

    data = get_comment_for_delete_function(user_name)
    media_id = get_post_id(user_name)
    if data['meta']['code'] == 200:
        if len(data['data']):
            for e in data:
                comment_id = data['data'][0]['id']
                comment_text = data['data'][0]['text']
            print comment_text
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
            print blob.sentiment
            if (blob.sentiment.p_neg>blob.sentiment.p_pos):
                print "Negative Comment : %s" %(comment_text)
                delete_url = (base_url + "media/%s/comments/%s?access_token=%s" %(media_id,comment_id,Access_Token))
                print "Delete URL is : %s" %delete_url
                delete_comment = requests.delete(delete_url).json()
                if delete_comment['meta']['code'] == 200 :
                    print "Comment Successfully Deleted!"
                else :
                    print "Unable To Delete Comment"
            else:
                print "Positive Comment : %s" %(comment_text)
            return blob.sentiment
            exit()
        else:
            print "No Comment"
    else:
        print "Status Code Other than 200 Recieve"

def get_negative_percentage():

    '''
    1.get a word
    2.call for textblob
    3.evaluate
    '''

    word = raw_input("Enter A word : ")
    b = TextBlob(word)
    print b.sentiment
    return b.sentiment
def get_comment_id(user_name):

    '''
    1.get post id
    2.create url
    3.fetch information
    '''

    post_id = get_post_id(user_name)
    request_url = base_url + 'media/%s/comments?access_token=%s' %(post_id,Access_Token)
    print request_url
    data = requests.get(request_url).json()
    print data['data'][0]['id']
    return data.keys()


def draw_a_chart_example():

    labels = 'tag1','tag2','tag3','tag4'
    sizes = [15, 30, 45, 10]
    explode = (0, 0, 0.1, 0)  # only "explode" the 3rd slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def get_recent_posts_tags_list (user_name):

    user_id = get_user_id(user_name)
    requested_url = base_url + "users/%s/media/recent/?access_token=%s" % (user_id, Access_Token)
    posts = requests.get(requested_url).json()['data']
    caption = []
    '''
    print collections.Counter(posts.split("#"))
    return collections.Counter(posts.split())
    '''

    for e in posts:
        caption.append(e['caption']['text'])
    print caption
    caption = []
    print len(caption)

    print collections.Counter(caption)
    return collections.Counter(caption)


def get_user_interests_hashtag_based_chart():


    #no idea how to complete this function  : -(  Need more time


    '''
    1.get a list of hashtags
    2.write some code to count the maximum used tags
    3.create a chart for most used hashtags
    4.fetch information about user interests from analysis
    :return: user interests
    '''
    return None

def startbot():
    '''
    1.create a menu
    2.take input from user
    2.call the function through menu options
    '''

    print "\n"
    print "           Hey!\n****Welcome to InstaBot****\n"
    print "Choose from Your Menu Options =>\n"
    print "a.Get your own Details"
    print "b.Get Details of Another User"
    print "c.Get my recent post"
    print "d.Download own posts"
    print "e.Download Another user's post"
    print "f.Post a Like"
    print "g.Post a Comment"
    print "h.Get Comments of User"
    print "i.Get media Liked by user"
    print "j.Get Tag Object Information"
    print "k.Get Recent Tagged media"
    print "l.Search tag by Name"
    print "m.Print sentiments and Delete Comment"
    print "n.Get negative percentage of a word"
    print "o.Draw a Example Pie-chart"
    print "p.Get Hashtags used by user"
    print "q.Get user's Interests"
    print "n.exit\n"



    choice = raw_input("Enter Your Choice...\n")
    if choice == "a" :
        self_info()
    if choice == "b" :
        user_name = raw_input("Enter the UserName Of the User>>>\n")
        get_user_info(user_name)
    if choice == "c" :
        get_own_post()
        exit()
    if choice == "d" :
        download_own_posts()
        exit()
    if choice == "e" :
        user_name = raw_input("Enter the UserName Of the User>>>\n")
        get_another_user_recent_post(user_name)
        exit()
    if choice == "f" :
        user_name = raw_input("Enter the name of the User>>")
        like_a_post(user_name)
        exit()
    if choice == "g" :
        user_name = raw_input("Enter the name of the User>>")
        post_a_comment(user_name)
        exit()
    if choice == "h" :
        user_name = raw_input("Enter the name of the User>>")
        get_comment(user_name)
        exit()
    if choice == "i" :
        media_liked_by_user()
        exit()
    if choice == "j" :
        tag_name = raw_input("Enter the Name Of Tag : ")
        tag_object_information(tag_name)
        exit()
    if choice == "k" :
        tag_name = raw_input("Enter the Name Of Tag : ")
        recent_tagged_media(tag_name)
        exit()
    if choice == "l" :
        tag_name = raw_input("Enter the Name Of Tag : ")
        search_tag_by_name(tag_name)
        exit()
    if choice == "m" :
        user_name = raw_input("Enter the User_Name : ")
        delete_negative_comment(user_name)
        exit()
    if choice == "n" :
        user_name = raw_input("Enter the name of the User>>")
        get_comment_id(user_name)
        exit()
    if choice == "o" :
        draw_a_chart_example()
        exit()
    if choice == "x" :
        get_negative_percentage()
        exit()
    if choice == "p" :
        user_name = raw_input("Enter name :")
        get_recent_posts_tags_list(user_name)
        exit()
    if choice == "q" :
        get_user_interests_hashtag_based_chart()
        exit()
    elif choice == "z" :
        exit()
    else :
        print "Wrong Choice"
startbot()


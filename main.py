import requests
import urllib
import textblob
from textblob.sentiments import NaiveBayesAnalyzer

import nltk

APP_ACCESS_TOKEN ='4870715640.a48e759.874aba351e5147eca8a9d36b9688f494'
BASE_URL='https://api.instagram.com/v1/'

        #----Function for getting user's own information----#


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if 'data' in user_info:

            print 'Username: %s' % (user_info['data']['username'])

            print 'Full name: %s ' % (user_info['data']['full_name'])

            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])

            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])

            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:

            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'




#------------function to get UserId ------------#


def get_user_id(insta_username):

    request_url = request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print "get request url: %s" % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
            print user_info['data'][0]['id']
        else:
            return None


    else:
        print 'status code other than 200.'
        exit()



#----------function to get info of a user using username--------#


def get_user_info(insta_username):

    user_id = get_user_id(insta_username)

    if user_id == None:

        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if 'data' in user_info:

            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])

        else:

            print 'There is no data for this user!'
    else:

        print 'Status code other than 200 received!'

#------------Function for getting own recent insta post--------------#


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:

        if len(own_media['data']):

            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)

            print 'Your image has been downloaded!'

        else:

            print 'Post does not exist!'
    else:

        print 'Status code other than 200 received!'

#-----------function to get recent post of a user by username-----------------#


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:

        if len(user_media['data']):

            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return user_media['data'][0]['id']

        else:

            print 'Post does not exist!'
    else:

        print 'Status code other than 200 received!'
        return None


#-------------Function for liking a post-------------#


def like_a_post(insta_username):

        media_id = like_a_post(insta_username)

        request_url = (BASE_URL + 'media/%s/likes') % (media_id)
        payload = {"access_token": APP_ACCESS_TOKEN}
        print 'POST request url : %s' % (request_url)
        post_a_like = requests.post(request_url, payload).json()

        if post_a_like['meta']['code'] == 200:

            print 'Your Like was successful!'

        else:

            print 'Your like was unsuccessful. Try again!'



#-----------Comment list--------------#

def get_comment_list(insta_username):

    media_id = get_user_post(insta_username)

    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    get_comment = requests.post(request_url, payload).json()

    if get_comment['meta']['code'] == 200:

        if 'data' in get_comment:

            print 'List Of Comments Is As Follows : '
            print "Comment is : %s By %s" % (get_comment['data'][0]['text'],get_comment['data'][0]['from'][1])

        else:

            print "No Comments Found!!"

    else:

        print 'Your request to display list of comments was unsuccessful.'


#-------function for deleting a post-----------#


def delete_negative_comments(insta_username):

	media_id = get_recent_post(insta_username)
	request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
	print 'GET request url : %s' % (request_url)
	comment_info = requests.get(request_url).json()

	if comment_info['meta']['code'] == 200:

		if len(comment_info['data']) > 0:           # Check if we have comments on the post

			for comment in comment_info['data']:    # If yes read them using for loop

			    comment_text = comment['text']
			    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

			    if blob.sentiment.p_neg > blob.sentiment.p_pos:

					comment_id = comment['id']
					delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
						media_id, comment_id, APP_ACCESS_TOKEN)
					print 'DELETE request url : %s' % (delete_url)

					delete_info = requests.delete(delete_url).json()

					if delete_info['meta']['code'] == 200:

						print 'Comment successfully deleted!'

					else:

						print 'Could not delete the comment'

		else:

			print 'No comments found'

	else:

		print 'Status code other than 200 received!'


#-----------MENU BAR------------#


def start_bot():
    choice = True
    while choice == True:

     print'Welcome to my INSTABOT'
     print 'Please choose one from the following menu options!!!'
     print '1.Get your own details. \n 2.Get user\'s details by the username.\n 3. Get own recent instagram post.\n 4. Get recent post of a user by username.\n 5.like a post on instagram.\n 6.List the comments on a post.\n 7.Delete the negative comments.\n 8.Close application.'
     option = input('Enter your choice:')

     if option == 1:
         self_info()
     elif option ==2:
         insta_username = raw_input("Enter the username of the user: ")
         get_user_id(insta_username)
     elif option == 3:
         get_own_post()
     elif option == 4:
         insta_username = raw_input("Enter the username of the user: ")
         get_user_post(insta_username)
     elif option ==5:
         insta_username = raw_input("Enter the username of the user: ")
         like_a_post(insta_username)
     elif option ==6:
         insta_username = raw_input("Enter the username of the user: ")
         get_comment_list(insta_username)
     elif option == 7:
         insta_username = raw_input("Enter the username of the user: ")
         delete_negative_comments(insta_username)
     elif option == 8:
         choice = False


start_bot()







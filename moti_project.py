
import json 
import datetime
import csv
import time
import requests
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
from random import randint
from twilio.rest import Client


app_id = "381373792260126"
app_secret = "02112d6ea1fdf09d9ff7268aa505238f"

access_token = app_id + "|" + app_secret

#since we want to scrape data about going on a run, let's try Nike.com 

page_id = 'nike'

# let's check that this page id is valid and the access token actually works

def testFBpagedata(page_id, access_token): 
	#make the URL string 
	base = "https://graph.facebook.com/v2.4"
	node = "/" + page_id
	parameters = "/?access_token=%s" % access_token
	url = base + node + parameters

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	data = json.loads(response.read().decode("utf-8"))

	print (json.dumps(data, indent = 4, sort_keys=True))

testFBpagedata(page_id, access_token)

#if the URL produces an error, keep requesting until it suceeds. 
def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print (e)
            time.sleep(5)
            
            print ("Error for URL %s: %s" % (url, datetime.datetime.now()))

    return response.read()
# this however, yields the id, and the name, (i.e) the facebook PAGE metadata, and we need to
# change the endpoint to the /feed endpoint to get the POST metadata on the nike feed. 

def getFacebookPostData(page_id, access_token, num_statuses):
	# construct the URL string 
	base = "https://graph.facebook.com"
	node = "/" + page_id + "/feed" 
	parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
	url = base + node + parameters

    # retrieve data
	data = json.loads((request_until_succeed(url)).decode("utf-8"))
	return data
    

test_status = getFacebookPostData(page_id, access_token, 1)['data'][0]
print (json.dumps(test_status['message'], indent=4, sort_keys=True))

# this reduces the number of posts requested to 1 (just to keep it clean), and makes 
# specific requests as to what data we want from the post. 

# now we want to process this data. We need to scrape for the intent of going on a run. 
# the status is now a dictionary of the metadata. Some keys may not exist, so we have to check
# for existance. 

def getFacebookPageFeedUrl(base_url):

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    # Reactions parameters
    fields = "&fields=message,link,created_time,type,name,id," + \
        "comments.limit(0).summary(true),shares,reactions" + \
        ".limit(0).summary(true)"

    return base_url + fields

def processFacebookPageStatus(status):
	status_id = status['id']
	status_message = '' if 'message' not in status.keys() else status['message'].encode('utf-8')

	link_name = '' if 'name' not in status.keys() else status['name'].encode('utf-8')
	status_type = status['type']
	status_link = '' if 'link' not in status.keys() else status['link']

	status_time = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
	status_time = status_time + datetime.timedelta(hours=-5) # EST
	status_time = status_time.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs

	num_likes = 0 if 'likes' not in status.keys() else status['likes']['summary']['total_count']
	num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
	num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']

	return (status_id, status_message,link_name, status_type, status_link,
       status_time, num_likes, num_comments, num_shares)


# # Now we have the tools to get the status information, and so we nned to write all this data to a CSV

def scraper(page_id, access_token):
	with open('%s_facebook_statuses.csv' % page_id, 'w') as file:
		w = csv.writer(file)
		w.writerow(["status_id", "status_message", "link_name", "status_type", "status_link","status_time", "num_likes", "num_comments", "num_shares"])

		has_next_page = True
		num_processed = 0   # keep a count on how many we've processed
		scrape_starttime = datetime.datetime.now()

		print ("Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime))

		after = ''
		base = "https://graph.facebook.com/v2.9"
		node = "/{}/posts".format(page_id)
		parameters = "/?limit={}&access_token={}".format(100, access_token)

		rand = randint(1, 300)

		while has_next_page:

			after = '' if after is '' else "&after={}".format(after)
			base_url = base + node + parameters + after

			url = getFacebookPageFeedUrl(base_url)
			statuses = json.loads(request_until_succeed(url).decode("utf-8"))
			
			for status in statuses['data']:
				w.writerow(processFacebookPageStatus(status))
		        
		        # output progress occasionally to make sure code is not stalling
				num_processed += 1
				if num_processed % 1000 == 0:
					print ("%s Statuses Processed: %s" % (num_processed, datetime.datetime.now()))
				if num_processed == rand: 
					random_message = status['message']
					print(random_message)
					print(rand)
					print(num_processed)
		    # if there is no next page, we're done.
			if 'paging' in statuses.keys():
				after = statuses['paging']['cursors']['after']
			else:
				has_next_page = False
	print ("\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime))
	return random_message
random_message = scraper(page_id, access_token)

account_sid = "AC64c88234fd07f2b3c978dd24777f53d1"
auth_token  = "859e2138b210f9f5c5c247df58891669"
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+19259892332", 
    from_="+19258923074",
    body= str(random_message))

print(message.sid)



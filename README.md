# Facebook Page Scraper

How to run the project: 

1) Pick what Facebook page you would like to scrape. Navigate to that Facebook page. 
You will see a url at the top, ex: https://www.facebook.com/nike/. Notice in the example
url I posted, there is a resource name, in my case, it is "nike". 

2) Take the resource name you found and set the variable "page_id" in the moti_project.py file
equal to it. 

3) Install the python twillo library using this command: pip install twilio

4) Run the page_scraper.py file on terminal using the command, python3 ./moti_project.py. This will:
	a) output all the scraped posts, along with the data from each post (number of likes, 
		time posted, message contained within, etc.) to a csv file. 
	b) send a text message containing a random scraped message to 978-618-6820.

5) Take the csv file and convert it to a json file using http://www.convertcsv.com/csv-to-json.htm

6) Install the firebase-import module locally using the terminal commands: 
	$ npm install firebase-import
	$ export PATH=$PATH:`npm bin`

7) Run the json_uploader.py program to upload this json file to firebase. The firebase url that
was used for this project was https://moti-codingchal.firebaseio.com, and the converted json file
was called convertedcsv_nike.json in my example. I inputted those pieces of information as arguments
to this second program as shown by running the command below. Running this will upload your json 
file to your firebase database. 

	python3 json_uploader.py https://moti-codingchal.firebaseio.com convertedcsv_nike.json
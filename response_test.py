try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
	
response = urllib2.urlopen('http://python.org/')
html = response.read()

print(html)
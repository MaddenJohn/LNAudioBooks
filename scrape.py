# This file is to test the scraping locally


# Scraping for novelfull.com
import requests
from bs4 import BeautifulSoup
import html

# currentHref = "/library-of-heavens-path/chapter-1637-a-breakthrough-in-soul-cultivation.html"
currentHref = "/library-of-heavens-path/chapter-1636-has-the-jiang-clan-betrayed-mankind-too.html"
# currentHref = "/library-of-heavens-path/chapter-1635-refining-the-ancient-sage-corpse.html"
domain = "http://novelfull.com"
url = domain + currentHref
response = requests.get(url)
text = html.unescape(response.text)
soup = BeautifulSoup(text, "html.parser")
for script in soup("script"):
	script.decompose()
for div in soup.find_all("div", {'class':'hidden'}):
	div.decompose()
	hidden.decompose()
tableNextChap = soup.select("#next_chap")
# nextHref = str(tableNextChap[0]['href'])
# nextChapURL = domain + nextHref
# print (nextChapURL)
table = soup.findAll('div',attrs={"class":"cha-words"})
# table = soup.findAll('div',attrs={"id":"chapter-content"})
print (table[0].text)

# import requests
# from bs4 import BeautifulSoup
# url = "https://light-novel.online/library-of-heavens-path/chapter-1485"
# r = requests.get(url, verify=True)
# status = r.status_code
# if (status == 200 ):
# 	soup = BeautifulSoup(r.text, "html.parser")
# 	for script in soup("script"):
# 	    script.decompose()
# 	for div in soup.find_all("div", {'class':'hidden'}):
# 		div.decompose()
# 		hidden.decompose()

# 	table = soup.findAll('div',attrs={"id":"chapter-content"})
# 	print (table)
# 	if "is coming soon!" in table[0].text:
# 		print ("Not found")
# 	print (table[0].text)
# else:
# 	print ("Error Calling url: " + url)




# import ssl
# from mechanize import Browser
#
# ssl._create_default_https_context = ssl._create_unverified_context
# b = Browser()
# b.set_handle_robots(False)
# b.addheaders = [('Referer', 'https://www.reddit.com'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# url = "https://light-novel.online/library-of-heavens-path/chapter-1485"
# b.open(url)
# if (b.response().code == 200):
# 	soup = BeautifulSoup(b.response().read(), "html.parser")
# 	for script in soup("script"):
# 	    script.decompose()
# 	for div in soup.find_all("div", {'class':'hidden'}):
# 		div.decompose()
# 		hidden.decompose()
# 	table = soup.findAll('div',attrs={"id":"chapter-content"})
# 	print (table)
# 	if not table[0] or len(table[0].text) < 100:
#         print ("Not found")
#         return 0
# 	print (table[0].text)
# else:
# 	print ("Error in open")

import requests
from bs4 import BeautifulSoup

x=1390
url = 'https://www.readlightnovel.org/ilibrary-of-heavens-path/chapter-' + str(x) + '/'
r = requests.get(url, verify=True)



if (r.status_code == 200):
	soup = BeautifulSoup(r.text, "html.parser")
	for script in soup("script"):
	    script.decompose()

	table = soup.findAll('div',attrs={"class":"chapter-content3"})

	print table[0].text.encode('utf8')
else:
	print ("Error Calling url: " + url)



import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key, Attr
import requests
from bs4 import BeautifulSoup
import ssl
from mechanize import Browser



# Add this chapter to the Database
def update(event, text):
    novel = event["novel"]
    ch = event["chapter"]
    recordId = novel + " " + ch
    # recordId = str(uuid.uuid4())
    voice = event["voice"]

    print('Generating new DynamoDB record, with ID: ' + recordId)
    if (len(text) > 30):
        print('Input Text: ' + text[0:25])
    else:
        print('Input Text: ' + text)
    print('Selected voice: ' + voice)
    
    #Creating new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.put_item(
        Item={
            'id' : recordId,
            'text' : text,
            'voice' : voice,
            'status' : 'PROCESSING'
        }
    )
    
    #Sending notification about new post to SNS
    client = boto3.client('sns')
    client.publish(
        TopicArn = os.environ['SNS_TOPIC'],
        Message = recordId
    )
    return recordId

# Update the record in the Database to a new number
def updateRecord(update,table,newChapter,title):
    if(update):
        print('Updating ' + title + ' to: ' + str(newChapter))
        table.update_item(Key={'Title':title},AttributeUpdates={'Ch':{'Value':newChapter,'Action':'PUT'}})

#scrape for a specific novel and chapter        
def scrape(event, novel, chapter, dynoTable, url):
    ssl._create_default_https_context = ssl._create_unverified_context
    b = Browser()
    b.set_handle_robots(False)
    b.addheaders = [('Referer', 'https://www.reddit.com'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    b.open(url)
    if (b.response().code == 200):
        soup = BeautifulSoup(b.response().read(), "html.parser")
        for script in soup("script"):
            script.decompose()
        for div in soup.find_all("div", {'class':'hidden'}):
            div.decompose()
            hidden.decompose()
        table = soup.findAll('div',attrs={"id":"chapter-content"})
        if not table[0] or len(table[0].text) < 100:
            print ("Not found")
            return 0
        text = table[0].text
        text = novel + " " + chapter + " " + text
        update(event, text)
        print ("New chapter found on website. Scraping is successful.")
        updateRecord(True, dynoTable, int(chapter) + 1, novel)
        return 1
    else:
        print ("Error returning url: " + url)
        return 0

'''
Helper lambda for the update lambda
'''
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_INDEX'])
    novel = event["novel"]
    ch = event["chapter"]
    url = event["url"]
    #Scrape new chapters and update databases
    update = scrape(event, novel, ch, table, url)
    return update

    
    
    
    
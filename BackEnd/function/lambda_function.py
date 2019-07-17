import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key, Attr
import requests
from bs4 import BeautifulSoup


# Add this chapter to the Database
def update(event, context, text):
    
    recordId = str(uuid.uuid4())
    voice = event["voice"]

    print('Generating new DynamoDB record, with ID: ' + recordId)
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
def scrape(novel, chapter, dynoTable):
    if (novel == 'LHP'):
        url = 'https://www.readlightnovel.org/library-of-heavens-path/chapter-' + str(chapter) + '/'
    if (novel == 'OG'):
        url = 'https://www.readlightnovel.org/overgeared/chapter-' + str(chapter) + '/'
    if (novel == 'SS'):
        url = 'https://www.readlightnovel.org/im-really-a-superstar/chapter-' + str(chapter) + '/'
        
    r = requests.get(url, verify=True)
    if (r.status_code == 200):
        soup = BeautifulSoup(r.text, "html.parser")
        for script in soup("script"):
            script.decompose()
    
        table = soup.findAll('div',attrs={"class":"chapter-content3"})
    
        text = table[0].text.encode('utf8')
        update(event, context, text)
        print ("New chapter found on website. Scraping is successful.")
        updateRecord(True, dynoTable, chapter + 1, novel)
        return 1
    else:
        print ("Error returning url: " + url)
        return 0

# Main function for handling the API call. This should get the current chapters
# scrape new chapters and then update the database with these new chapters.
def lambda_handler(event, context):
    
    #Getting current Chapters
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_INDEX'])
    #LHP, OG, SS
    LHP_Chapter = table.get_item(Key={'Title':'LHP'},AttributesToGet=['Ch'])['Item']['Ch']
    print('Current Library of Heaven\'s Path Chapter: ' + str(LHP_Chapter))
    OG_Chapter = table.get_item(Key={'Title':'OG'},AttributesToGet=['Ch'])['Item']['Ch']
    print('Current Overgeared Chapter: ' + str(OG_Chapter))
    SS_Chapter = table.get_item(Key={'Title':'SS'},AttributesToGet=['Ch'])['Item']['Ch']
    print('Current Superstar Chapter: ' + str(SS_Chapter))
    
    #Scrape new chapters and update databases
    updateLHP = scrape('LHP', LHP_Chapter, table)
    # updateOG = scrape('OG', OG_Chapter, table)
    # updateSS = scrape('SS', SS_Chapter, table)
    
    return str(updateLHP + updateOG + updateSS) + " Chapters Updated"

    
    
    
    
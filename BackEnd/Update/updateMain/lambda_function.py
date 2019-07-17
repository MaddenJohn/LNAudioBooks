import boto3
import os
import uuid
import json
from boto3.dynamodb.conditions import Key, Attr

'''
Function to get url
'''
def getURL(novel, chapter):
    if (novel == 'LHP'):
        url = 'https://light-novel.online/library-of-heavens-path/chapter-' + str(chapter)
    if (novel == 'OG'):
        url = 'https://light-novel.online/library-of-heavens-path/chapter-' + str(chapter)
    if (novel == 'SS'):
        url = 'https://light-novel.online/im-really-a-superstar/chapter-' + str(chapter)
    if (novel == 'LU'):
        url = 'https://light-novel.online/only-i-level-up/chapter-' + str(chapter)
    if (novel == 'RTW'):
        url = 'https://light-novel.online/release-that-witch/chapter-' + str(chapter)
    return url

'''
Function to call helper lambda.
'''
def callHelper(event, context, novel, chapter, url):
    client = boto3.client('lambda')
    payload = {
        "voice" : event['voice'],
        "novel" : novel,
        "chapter" : str(chapter),
        "url" : url
    }
    payload = json.dumps(payload)
    # use InvocationType=RequestResponse for synchronous,
    # use InvocationType=Event for asynchronous,
    response = client.invoke(FunctionName='updateHelper', InvocationType='Event', Payload=payload)
    return response

# Main function for handling the API call. This should get the current chapters
# scrape new chapters and then update the database with these new chapters.
def lambda_handler(event, context):

    #Getting current Chapters
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_INDEX'])
    #LHP, OG, SS
    LHP_Chapter = table.get_item(Key={'Title':'LHP'},AttributesToGet=['Ch'])['Item']['Ch']
    print('Current Library of Heaven\'s Path Chapter: ' + str(LHP_Chapter))
    # OG_Chapter = table.get_item(Key={'Title':'OG'},AttributesToGet=['Ch'])['Item']['Ch']
    # print('Current Overgeared Chapter: ' + str(OG_Chapter))
    SS_Chapter = table.get_item(Key={'Title':'SS'},AttributesToGet=['Ch'])['Item']['Ch']
    print('Current Superstar Chapter: ' + str(SS_Chapter))
    LU_Chapter = table.get_item(Key={'Title':'LU'},AttributesToGet=['Ch'])['Item']['Ch']
    print('Current Level Up Chapter: ' + str(LU_Chapter))
    RTW_Chapter = table.get_item(Key={'Title':'RTW'},AttributesToGet=['Ch'])['Item']['Ch']
    print('Current Release that Witch Chapter: ' + str(RTW_Chapter))

    LHP2_Chapter = table.get_item(Key={'Title':'LHP2'},AttributesToGet=['Ch'])['Item']['Ch']
    urlLHP2 = table.get_item(Key={'Title':'LHP2'},AttributesToGet=['url'])['Item']['url']
    print('Current Library of Heaven\'s Path Chapter: ' + str(LHP_Chapter) + ' ' + str(urlLHP2))


    urlLHP = getURL('LHP', LHP_Chapter)
    urlSS = getURL('SS', SS_Chapter)
    urlLU = getURL('LU', LU_Chapter)
    urlRTW = getURL('RTW', RTW_Chapter)
    #Scrape new chapters and update databases
    # updateLHP = callHelper(event, context, 'LHP', LHP_Chapter, urlLHP)
    updateLHP2 = callHelper(event, context, 'LHP2', LHP2_Chapter, urlLHP2)
    # updateOG = scrape('OG', OG_Chapter)
    updateSS = callHelper(event, context, 'SS', SS_Chapter, urlSS)
    # updateLU = callHelper(event, context, 'LU', LU_Chapter, urlLU)
    # updateRTW = callHelper(event, context, 'RTW', RTW_Chapter, urlRTW)

    return "Chapters Updated"

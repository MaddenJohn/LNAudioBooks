import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):

    postId = event["postId"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    print ("Search Query: " + str(postId))

    if postId=="*":
        items = table.scan()
        print ("Showing Entire DB of this many items: " + str(len(items["Items"])))
    else:
        items = table.query(
            KeyConditionExpression=Key('id').eq(postId)
        )
        print ("Showing DB of single item")

    return items["Items"]

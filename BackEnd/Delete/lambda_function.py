import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    print(event, context)
    postId = event["postId"]
    print('Deleting new DynamoDB record, with ID: ' + postId)

    #Deleting new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.delete_item(
        Key={
            'id' : postId
        }
    )
    location = "Bucket=" + os.environ['BUCKET_NAME'] + " Key=  " + postId + ".mp3"
    print('Deleting  S3 object, with: ' + location)
    #Deleting mp3 object in S3
    s3 = boto3.client('s3')
    s3.delete_object(Bucket=os.environ['BUCKET_NAME'], Key=postId + ".mp3")
    return postId

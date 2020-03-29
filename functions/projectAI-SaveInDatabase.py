import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    logger.info("Saving data in Database...")
    logger.info(f'Input event: {event}')

    # Adding information about new audio file to DynamoDB table
    table = dynamodb.Table(os.environ['DB_NAME'])
    table.put_item(
        Item={
            'name': event['key'][:-4],
            'text': event['content'],
            'Language': event['language'],
            'voice': event['voice'],
            'link': event['link']
        }
    )

    return "OK"

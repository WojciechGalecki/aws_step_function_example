import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')


def lambda_handler(event, context):
    logger.info("Sending message...")
    logger.info(f'Input event: {event}')

    sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Message=event['link'],
        Subject='New audio file'
    )

    return "OK"

import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')


def lambda_handler(event, context):
    logger.info("Adding message to queue...")
    logger.info(f'Input event: {event}')

    sqs.send_message(
        QueueUrl=os.environ['SQS_URL'],
        MessageBody=event['link']
    )

    return "OK"

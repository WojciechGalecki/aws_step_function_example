import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('stepfunctions')


def lambda_handler(event, context):
    logger.info('Detecting file type')
    logger.info(f'Input event: {event}')

    bucket = event['bucket']
    key = event['key']
    type = key[-3:]

    logger.info(f'Type: {type}')

    return {'bucket': bucket, 'key': key, 'type': type}

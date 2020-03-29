import boto3
import logging
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('stepfunctions')


def lambda_handler(event, context):
    logger.info('Creating new Step Functions execution')
    logger.info(f'Input event: {event}')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    logger.info(f'Bucket: {bucket}')
    logger.info(f'Key: {key}')

    response = {'bucket': bucket, 'key': key}

    client.start_execution(
        stateMachineArn=os.environ['STEPFUNCTION_ARN'],
        input=json.dumps(response),
    )

    return 'OK'

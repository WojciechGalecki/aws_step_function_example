import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rekognition = boto3.client('rekognition')


def lambda_handler(event, context):
    logger.info("Analazying image...")
    logger.info(f'Input event: {event}')

    # Invoke Rekognition service
    response = rekognition.recognize_celebrities(
        Image={
            'S3Object': {
                'Bucket': event['bucket'],
                'Name': event['key']
            }
        }
    )

    celebrity = response['CelebrityFaces'][0]['Name']

    event['celebrity'] = celebrity

    return event

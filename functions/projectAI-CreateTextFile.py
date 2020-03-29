import boto3
import logging
import io

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')


def lambda_handler(event, context):
    logger.info("Creating text file...")
    logger.info(f'Input event: {event}')

    text = 'I see ' + event['celebrity'] + ' on the picture dude!'
    fileName = event['key'][:-4] + ".txt"

    with io.FileIO("/tmp/" + fileName, "w") as file:
        file.write(text.encode())

    # Save a file with description in S3
    s3.upload_file('/tmp/' + fileName, event['bucket'], fileName)

    return "OK"

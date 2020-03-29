import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')
comprehend = boto3.client('comprehend')


def lambda_handler(event, context):
    logger.info("Detecting language...")
    logger.info(f'Input event: {event}')

    bucket = event['bucket']
    key = event['key']

    # Saving file in local directory
    s3.meta.client.download_file(bucket, key, "/tmp/" + key)

    # Reading a file
    with open("/tmp/" + key, 'r') as myfile:
        content = myfile.read().replace('\n', ' ')

    # Detect language
    response = comprehend.detect_dominant_language(
        Text=content
    )

    language = response['Languages'][0]['LanguageCode']
    logger.info(f'Language: {language}')

    return {'bucket': bucket, 'key': key, 'language': language, 'content': content}

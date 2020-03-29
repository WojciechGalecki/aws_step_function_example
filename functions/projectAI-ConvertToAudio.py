import boto3
import logging
import os
from contextlib import closing

logger = logging.getLogger()
logger.setLevel(logging.INFO)

polly = boto3.client('polly')
s3 = boto3.client('s3')

languages = {'en': 'Kendra',
             'pl': 'Jacek',
             'de': 'Hans',
             'fr': 'Celine',
             'jp': 'Mizuki'
             }


def lambda_handler(event, context):
    logger.info("Converting to audio...")
    logger.info(f'Input event: {event}')

    language = event['language']
    bucket = event['bucket']
    key = event['key']
    content = event['content']
    voice = 'Kendra'
    if languages.keys().__contains__(language):
        voice = languages[language]

    # Using Amazon Polly service to convert text to speech
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=content,
        TextType='text',
        VoiceId=voice
    )

    # Save audio on local directory
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join("/tmp/", key)
            with open(output, "wb") as file:
                file.write(stream.read())

    # Save audio file on S3
    newKey = key[:-4] + ".mp3"
    s3.upload_file('/tmp/' + key, bucket, newKey)
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=newKey)

    location = s3.get_bucket_location(Bucket=bucket)
    region = location['LocationConstraint']
    link_begining = f'https://s3-{str(region)}.amazonaws.com/'
    link = f'{link_begining}{bucket}/{newKey}'

    event['newKey'] = newKey
    event['link'] = link
    event['voice'] = voice

    return event

import boto3
import json
import os
import logging

# Configure standardized system logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    polly = boto3.client('polly')

    # Read the exact new uppercase keys you defined in the Lambda Console
    source_bucket = os.environ.get('SOURCE_BUCKET')
    destination_bucket = os.environ.get('DESTINATION_BUCKET')

    # Safe S3 extraction with array indexing fixed
    text_file_key = event['Records'][0]['s3']['object']['key']
    
    # Ignore folder setups or accidental binary files in the source bucket
    if not text_file_key.lower().endswith('.txt'):
        logger.info(f"Skipping file without .txt extension: {text_file_key}")
        return {'statusCode': 200, 'body': json.dumps('File skipped')}

    # Safely swap out the extension text for the audio path payload
    audio_key = text_file_key.rsplit('.', 1)[0] + '.mp3'

    try:
        logger.info(f"Downloading text target from: {source_bucket}/{text_file_key}")
        text_file = s3.get_object(Bucket=source_bucket, Key=text_file_key)
        text_data = text_file['Body'].read().decode('utf-8')

        # Prevent empty payloads from reaching Polly
        if not text_data.strip():
            logger.warning("Aborting synthesis: Source text file is completely empty.")
            return {'statusCode': 200, 'body': json.dumps('Empty file skipped')}

        logger.info(f"Streaming text conversion payload to Amazon Polly")
        response = polly.synthesize_speech(
            Text=text_data,
            OutputFormat='mp3',
            VoiceId='Joanna',
            Engine='neural' # Upgraded to neural engine for maximum realism
        )

        # Streams raw file bytes straight to S3 memory to protect /tmp storage from space crashes
        if 'AudioStream' in response:
            logger.info(f"Writing audio stream to destination target: {destination_bucket}/{audio_key}")
            s3.put_object(
                Bucket=destination_bucket,
                Key=audio_key,
                Body=response['AudioStream'].read(),
                ContentType='audio/mpeg'
            )
        
        logger.info(f"Successfully processed audio generation lifecycle for: {audio_key}")
        return {
            'statusCode': 200,
            'body': json.dumps('Audio translation transaction completed successfully!')
        }
    
    except Exception as e:
        logger.error(f"Execution pipeline failure for file {text_file_key}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Pipeline error encountered: {str(e)}')
        }

#lambda_functions

#DECODE
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    print(event)

    # Get the s3 address from the Step Function event input
    key = event['key']
    bucket = event['bucket']

    # Download the data from s3 to /tmp/image.png
    s3.download_file( bucket, key ,'/tmp/image.png')


    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }



#INVOKE ENDPOINT
import json
import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2021-12-17-09-55-58-492"

#"image-classification-2021-12-15-20-12-17-120"
def lambda_handler(event, context):
   # Decode the image data
    body = event['body']
    image = base64.b64decode(event['body']['image_data']) ## TODO: fill in
    # Instantiate a Predictor
    runtime = boto3.client('runtime.sagemaker')
    
    # Make a prediction:
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType="image/png",Body=image)
    inferences = json.loads(response['Body'].read().decode('utf-8'))
    
    print("...inferences:", inferences)
    # We return the data back to the Step Function    
    return {
        'statusCode': 200,
        'body': {
            "inferences": inferences
        }
    }


#THRESHOLD
import json
THRESHOLD = .8

def lambda_handler(event, context):

    # Grab the inferences from the event
    ## TODO: fill in
    inferences = event['body']['inferences']

    # Check if any values in our inferences are above THRESHOLD
    if (max(inferences) >= THRESHOLD):
        meets_threshold = True
    else:
        meets_threshold = False
    ## TODO: fill in

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

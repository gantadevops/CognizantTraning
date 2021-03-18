import boto3
sns = boto3.client('sns')
# Publish a simple message to the specified SNS topic
response = sns.publish(
    TopicArn='arn:aws:sns:us-east-2:101048863733:alerts',
    Message='Hello World',   
)

# Print out the response
print(response)
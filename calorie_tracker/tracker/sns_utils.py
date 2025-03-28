import boto3
from django.conf import settings


def send_meal_reminder():
    sns_client = boto3.client("sns", region_name=settings.AWS_REGION)

    message = "Hey! Don't forget to log your meal for today!"

    response = sns_client.publish(
        TopicArn=settings.AWS_SNS_TOPIC_ARN,
        Message=message,
        Subject="Meal Logging Reminder"
    )

    return response


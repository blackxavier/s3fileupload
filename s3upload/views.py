from django.shortcuts import render
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

# from urllib3 import request


def index(request):
    return render(request, "s3upload/index.html")


def upload_to_s3(file, bucket_name, object_name=None, request=None):
    """
    Upload a file to an S3 bucket

    :param file: File-like object to be uploaded
    :param bucket_name: Name of the S3 bucket
    :param object_name: S3 object name (key)
    :return: True if successful, else False
    """
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        if object_name is None:
            object_name = file.name

        s3_client.upload_fileobj(file, bucket_name, object_name, request)
        print(f"Successfully uploaded {object_name} to {bucket_name}")
        return True

    except NoCredentialsError:
        messages.error(request, "AWS credentials not available.")
        return False
    except Exception as e:
        messages.error(request, f"Error uploading to S3: {str(e)}")
        return False


def upload_file(request):
    if request.method == "POST":
        file = request.FILES["image"]
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        if upload_to_s3(file, bucket_name, request=request):
            print("Passed this area,upload_file")
            messages.success(request, "File uploaded successfully to S3!")
        else:
            messages.error(request, "Failed to upload file to S3.")

    return redirect("index")

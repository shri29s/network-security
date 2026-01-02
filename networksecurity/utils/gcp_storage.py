from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity import constants

from google.cloud import storage
from google.cloud.storage.transfer_manager import upload_many_from_filenames
import os

def save_to_bucket(source_file, destination_blob):
    try:
        bucket_name = constants.ARTIFACT_BUCKET_NAME

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob)

        blob.upload_from_filename(source_file)
        logging.info(f"Uploaded {source_file} to gs://{bucket_name}/{destination_blob}")
    except Exception as e:
        raise NetworkSecurityException(e)
    
def save_many_to_bucket(source_dir, bucket_prefix):
    try:
        bucket_name = constants.ARTIFACT_BUCKET_NAME
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        source_dir = os.path.abspath(source_dir)

        uploaded = 0
        for root, _, files in os.walk(source_dir):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, source_dir)
                rel_path = rel_path.replace("\\", "/")

                blob_name = f"{bucket_prefix}/{rel_path}"

                blob = bucket.blob(blob_name)
                blob.upload_from_filename(local_path)

                uploaded += 1

        logging.info(
            f"Uploaded {uploaded} files to "
            f"gs://{bucket_name}/{bucket_prefix}"
        )

    except Exception as e:
        raise NetworkSecurityException(e)


import json
import logging
from pathlib import Path
import os
from typing import Optional

from google.cloud import storage
from google.oauth2 import service_account

from ai_metaphors.server.settings.settings import settings


class GCSStorageService:
    """
    Service for handling file storage operations with Google Cloud Storage
    """

    def __init__(self):
        self.bucket_name = settings.BUCKET_NAME
        self.client = self._init_gcs_client()
        self.bucket = self.client.bucket(self.bucket_name)
        logging.info(f"Initialized GCS client for bucket {self.bucket_name}")

    @staticmethod
    def _init_gcs_client() -> storage.Client:
        """Initialize Google Cloud Storage client"""
        # Check if we have a service account key file
        if settings.KEY_JSON:
            # Use service account key file

            if os.path.exists(settings.KEY_JSON):
                credentials = service_account.Credentials.from_service_account_file(settings.KEY_JSON)
            else:
                credentials = service_account.Credentials.from_service_account_info(json.loads(settings.KEY_JSON))

            client = storage.Client(
                credentials=credentials,
                project=credentials.project_id
            )
            logging.info(f"Using service account from `key.json`")
            return client
        else:
            # Try to use default credentials
            logging.warning("No explicit credentials provided, using default credentials")
            return storage.Client()

    def upload_file(self, file_path: Path, object_key: str) -> Optional[str]:
        """
        Upload a file to GCS and return the URL

        Args:
            file_path: Path to the file to upload
            object_key: Key/path where the file will be stored in the bucket

        Returns:
            URL to access the uploaded file or None if upload failed
        """
        try:
            blob = self.bucket.blob(object_key)
            blob.upload_from_filename(str(file_path))

            # Generate a signed URL for the uploaded file
            url = blob.generate_signed_url(
                version="v4",
                expiration=settings.URL_EXPIRATION,
                method="GET"
            )

            logging.info(f"File uploaded successfully to GCS: {object_key}")
            return url
        except Exception as e:
            logging.error(f"Error uploading file to GCS: {str(e)}")
            return None
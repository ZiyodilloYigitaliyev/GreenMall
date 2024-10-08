import os

AWS_ACCESS_KEY_ID = "AKIA4ZPZVFKKGZUBZ5F2"
AWS_SECRET_ACCESS_KEY = "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"
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_STORAGE_BUCKET_NAME = "bucketmyway"
AWS_ENDPOINT_URL = "https://greenwall.fra1.digitaloceanspaces.com"
AWS_ENDPOINT = "fra1.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
DEFAULT_FILE_STORAGE = "core.cdn.backends.MediaRootS3Boto3Storages"
STATICFILES_STORAGE = "core.cdn.backends.StaticRootS3Boto3Storages"
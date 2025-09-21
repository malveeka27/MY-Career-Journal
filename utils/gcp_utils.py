from google.cloud import storage

#UPLOADS OBJECTS FROM STREAMLIT UPLOADER TO GCS(GOOGLE CLOUD STORAGE)
def upload_to_gcs(bucket_name, file, destination_blob_name):

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # UPLOAD THE FILE
    blob.upload_from_file(file, rewind=True)

    return f"gs://{bucket_name}/{destination_blob_name}"


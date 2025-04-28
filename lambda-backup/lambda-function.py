import boto3
import json
import datetime
import os
from pymongo import MongoClient

def lambda_handler(event, context):
    # MongoDB details
    mongo_uri = os.environ['mongodb+srv://reshma:reshma@cluster0.tgvel.mongodb.net/tm']
    
    # S3 details
    s3_bucket_name = os.environ['reshma-test-1']
    
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client.get_database()  # Use default database from URI

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Temporary backup file
    backup_file = f"/tmp/mongo-backup-{timestamp}.json"

    try:
        # Export collections
        backup_data = {}
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            documents = list(collection.find())
            # Convert ObjectId to string
            for doc in documents:
                doc['_id'] = str(doc['_id'])
            backup_data[collection_name] = documents

        # Write to JSON file
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f)

        # Upload to S3
        s3_client = boto3.client('s3')
        s3_client.upload_file(backup_file, s3_bucket_name, f"backups/mongo-backup-{timestamp}.json")

        return {
            'statusCode': 200,
            'body': f'Backup successful and uploaded to S3 as mongo-backup-{timestamp}.json'
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f'Backup failed: {str(e)}'
        }

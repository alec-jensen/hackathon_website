from pymongo import MongoClient
from dotenv import load_dotenv
import os
import argparse

parser = argparse.ArgumentParser(description='Get emails from the database')
parser.add_argument('--output', '-o', type=str, help='Output file path')
parser.add_argument('--type', '-t', type=str, help='Output file type', default='csv', choices=['csv', 'txt', 'json'])
parser.add_argument('--overwrite', '-ow', action='store_true', help='Overwrite the output file if it exists')

args = parser.parse_args()

load_dotenv()

MONGO_URL = os.getenv('MONGODB_URI')

client = MongoClient(MONGO_URL)

db = client["hackathon"]
collection = db["registrations"]

emails = []

for document in collection.find():
    if document.get("email"):
        emails.append(document["email"])

if args.output:
    if args.overwrite or not os.path.exists(args.output):
        if os.path.commonprefix([os.getcwd(), os.path.abspath(args.output)]) != os.getcwd():
            print('Invalid path')
            exit(1)

        with open(args.output, 'w') as file:
            if args.type == 'csv':
                file.write(','.join(emails))
            elif args.type == 'txt':
                file.write('\n'.join(emails))
            elif args.type == 'json':
                import json
                file.write(json.dumps(emails))
    else:
        print('File already exists. Use --overwrite to overwrite the file.')
else:
    print(", ".join(emails))

client.close()

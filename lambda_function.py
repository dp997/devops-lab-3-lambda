import pandas as pd
from sqlalchemy import create_engine
import boto3
import os
import urllib.parse

print("Imported packages")
rds = boto3.client('rds')
s3_client = boto3.client('s3')

print("Connected to AWS")
dbhostname = os.environ['DBHOSTNAME']
dbport = os.environ['DBPORT']
dbusername = os.environ['DBUSERNAME']
dbname = os.environ['DBNAME']

password = rds.generate_db_auth_token(DBHostname = dbhostname,
                                      Port = dbport,
                                      DBUsername = dbusername,
                                      Region = None)
                       
password = urllib.parse.quote(password)
print("Generated password")

def lambda_handler(event, context):
    if(event['dataset'] == 'Cars'):
        datalink = s3_client.get_object(Bucket=os.environ['DATASET_BUCKET'], Key="mtcars.csv")
    elif(event['dataset'] == 'Leaders'):
        datalink = s3_client.get_object(Bucket=os.environ['DATASET_BUCKET'], Key="european_leaders.csv")
    else:
        datalink = s3_client.get_object(Bucket=os.environ['DATASET_BUCKET'], Key="2014_apple_stock.csv")
    
    data = pd.read_csv(datalink['Body'])
    engine_string = f'postgresql+psycopg2://{dbusername}:{password}@{dbhostname}:{dbport}/{dbname}?sslmode=require'

    engine = create_engine(engine_string)

    conn = engine.connect()

    data.to_sql(
        name = "test_dataset",
        con = conn,
        if_exists = 'replace',
        index = False
    )
    conn.close()
    engine.dispose()

    return("Uploaded data.")

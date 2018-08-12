Working result
Write/Create a text file, copy it to another bucket and delete the original
```
import boto3
from io import StringIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Function to write text contents to a file
    # and read it back gain
    contents = 'My Goodness Goober string to save to S3 object'
    target_bucket = 'wildrydes-dave-coate'
    target_file = 'hello.txt'

    # Write to a file
    # notice if you do fake_handle.read() it reads like a file handle
    fake_handle = StringIO(contents)
    s3.put_object(Bucket=target_bucket, Key=target_file, Body=fake_handle.read())
    
    # Read the file back again
    data = s3.get_object(Bucket=target_bucket, Key=target_file)
    contents = data['Body'].read()
    print(contents)

    # Create object for the copy command
    copy_source = {
    'Bucket': target_bucket,
    'Key': target_file
    }

    # Set CopyTo: bucket and copy
    copy_to_bucket = 'coatedslmbdatest02'
    s3.copy_object(Bucket=copy_to_bucket, Key=target_file, CopySource=copy_source)

    # Delete the file from the wildrydes bucket
    s3.delete_object(Bucket=target_bucket, Key=target_file)
```

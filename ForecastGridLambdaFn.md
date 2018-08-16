# Forecast Grid Lambda Function
* coateds-forecast-grid-lambda

## Testing the role permissions to write to the bucket
Also included is a very simple function to write to the s3 bucket
```
import boto3
from io import StringIO

s3 = boto3.client('s3')

def writebuckettextfile(bucket, file, contents):
    # Write to a file
    # notice if you do fake_handle.read() it reads like a file handle
    fake_handle = StringIO(contents)
    s3.put_object(Bucket=bucket, Key=file, Body=fake_handle.read())

def lambda_handler(event, context):
    writebuckettextfile('coateds-forecast-grid-web', 'hello.txt', 'Some Content')
```

Intermediate Step: Generates a random number...

```
import random
import boto3
from io import StringIO

s3 = boto3.client('s3')

def writebuckettextfile(bucket, file, contents):
    # Write to a file
    # notice if you do fake_handle.read() it reads like a file handle
    fake_handle = StringIO(contents)
    s3.put_object(Bucket=bucket, Key=file, Body=fake_handle.read(), ContentType='text/html', ContentEncoding='utf-8')

def lambda_handler(event, context):
    rnd = str(random.randint(1, 99))
    content = f"<html><head><meta charset='utf-8'></head><body><h1>{rnd}</h1></body></html>"
    writebuckettextfile('coateds-forecast-grid-web', 'index.html', content)
```



Now schedule a task and verify the file changes every x min
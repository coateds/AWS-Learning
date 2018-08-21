# Create a Python/Lambda working environment on an EC2 instance
Goal: create a zip file that can be uploaded to AWS Lambda to create a new Python/Lambda function with dependencies. The first dependency is the import requests module required to read the OWM site

## The top level sequence is
1. Create an EC2 instance out of the Amazon Linux 2 AMI (Requires a 64-bit Amazon Linux instance)
  * Amazon AMIs come with Python 2.7... To work with 3.6 upgrade/installation is necessary
2. I am using my [normal personal username].pem for a key
3. from home dir of surface:  ssh -i [normal personal username].pem ec2-user@x.x.x.x
4. Prep the image if necessary with Python, PIP, Virtualenv, and requests (others?)
5. Paste the tested code into [function_name].py
6. Zip the dependencies into [function_name].py
7. Add the .py file to the zip file
8. Create a role if necessary
9. Run `aws lambda create-function` with options to build the function

## Install Python, PIP, Virtualenv and dependencies on EC2 instance
* source:  https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html
* from home dir of surface:  ssh -i [normal personal username].pem ec2-user@x.x.x.x
* `sudo yum install -y gcc zlib zlib-devel openssl openssl-devel`
* `wget https://www.python.org/ftp/python/3.6.1/Python-3.6.x.tgz`
  * Currently using 3.6.5, substitute this in commands
* `tar -xzvf Python-3.6.x.tgz`
* `cd Python-3.6.x && ./configure && make`
* `sudo make install`
* `sudo /usr/local/bin/pip3 install virtualenv`

Choose the virtual environment that was installed via pip3
* `/usr/local/bin/virtualenv ~/shrink_venv`
* `source ~/shrink_venv/bin/activate`

Install libraries in the virtual environment
* `pip install requests`
* `pip install pytz`

`cd ~`

## Python file minimums
```
import requests
import os
import sys
import datetime

def handler(event, context):
    print('anything')
```

## Add the contents of lib and lib64 site-packages and .py file to your .zip file
* `cd $VIRTUAL_ENV/lib/python3.6/site-packages`
* `zip -r9 ~/[function-name].zip .`
* `cd ~`
* `zip -g [function-name].zip [function-name].py `

## Create the credentials if necesary
* From home dir
* `aws configure` use creds for my AWS admin user

## Create the function
```
aws lambda create-function \
--region us-west-2 \
--function-name TestRequests \
--zip-file fileb:///home/ec2-user/TestRequests.zip \
--role arn:aws:iam::XXXXXXXXXXXX:role/service-role/lambda_s3 \
--handler TestRequests.handler \
--runtime python3.6 \
--timeout 10 --memory-size 1024
```

# Update the Python code process
* If the EC2 instance is stopped
  * Start it
  * Log on
  * 'Source' the venv
* Start here if the EC2 is a;ready running and configured
  * Update the .py file with new code
  * Delete/Recreate the zip file
* Delete the Lambda Function
  * `aws lambda create-function ...`
* Configure the function
  * enter the env variable
  * Create the test event
  * TEST!!

```
aws lambda update-function-code \
--function-name TestRequests \
--zip-file fileb:///home/ec2-user/TestRequests.zip
```

## Environment post first working (beta) release
* Prod lambda function
  * coatedsforecastgridlambda
  * execution role: coateds-forecast-grid-lambda-role
  * CloudWatch event: forecastgridscheduledevent
  * build on EC2 instance named "forecast grid"
  * pip list
    * Package    Version  
    * ---------- ---------
    * certifi    2018.8.13
    * chardet    3.0.4    
    * idna       2.7      
    * pip        18.0     
    * pytz       2018.5   
    * requests   2.19.1   
    * setuptools 40.0.0   
    * urllib3    1.23     
    * wheel      0.31.1  
* Dev lambda function
  * coatedsforecastgridlambda
  * execution role: service-role/lambda_s3
  * CloudWatch event: NONE
  * build on EC2 instance named "Test Requests"
  * pip list
    * Package    Version  
    * ---------- ---------
    * certifi    2018.4.16
    * chardet    3.0.4    
    * idna       2.7      
    * pip        18.0     
    * pytz       2018.5   
    * requests   2.19.1   
    * setuptools 40.0.0   
    * urllib3    1.23     
    * wheel      0.31.1 
* S3 web enabled bucket: coateds-forecast-grid-web

Improvements list
* "Last Run: "  timestamp - Done
  * code snippet in Dev
  * Consider building a function
* Clean up/refactor code
* place in frame of davecoate.com - 1/2 done
* apply styles to table - done
* Add weather locations (rafactor to make this easier?) - done

Testing the SAM CLI
* After setting up an environment like that above
* pip install aws-sam-cli
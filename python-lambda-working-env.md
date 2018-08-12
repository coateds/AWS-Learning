# Create a Python/Lambda working environment on an EC2 instance
Goal: create a zip file that can be uploaded to AWS Lambda to create a new Python/Lambda function with dependencies. The first dependency is the import requests module required to read the OWM site

## The top level sequence is
1. Create an EC2 instance out of the Amazon Linux 2 AMI (Requires a 64-bit Amazon Linux instance)
2. I am using my [normal personal username].pem for a key
3. from home dir of surface:  ssh -i coateds.pem ec2-user@34.214.227.227
4. Prep the image if necessary with Python, PIP, Virtualenv, and requests (others?)
5. Paste the tested code into [function_name].py
6. Zip the dependencies into [function_name].py
7. Add the .py file to the zip file
8. Create a role if necessary
9. Run `aws lambda create-function` with options to build the function

## Install Python, PIP, Virtualenv and dependencies on EC2 instance
* `sudo yum install -y gcc zlib zlib-devel openssl openssl-devel`
* `wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz`
  * This is NOT the latest version. It might be better to update to 3.6.5??
* `tar -xzvf Python-3.6.1.tgz`
  * or relevent version
* `cd Python-3.6.1 && ./configure && make`
* `sudo make install`
* `sudo /usr/local/bin/pip3 install virtualenv`

Choose the virtual environment that was installed via pip3
* `/usr/local/bin/virtualenv ~/shrink_venv`
* `source ~/shrink_venv/bin/activate`

Install libraries in the virtual environment
* `pip install requests`

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
--role arn:aws:iam::817967764457:role/service-role/lambda_s3 \
--handler TestRequests.handler \
--runtime python3.6 \
--timeout 10 --memory-size 1024
```
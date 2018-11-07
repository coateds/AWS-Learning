# There are two environments
* Dev: ec2:Test Requests > lambda:TestRequests > s3:coateds-forecast-grid-web
  * Test with 'TestRequest' test

## Make a change in Dev
* https://aws.amazon.com/
* Login to AWS with MapManDave@gmail.com
* start ec2 instance "Test Requests"
* ssh -i [normal personal username].pem ec2-user@x.x.x.x
* modify code in ~/TestRequests.py
* `source ~/shrink_venv/bin/activate`
* `cd $VIRTUAL_ENV/lib/python3.6/site-packages`
* `zip -r9 ~/TestRequests.zip .`
* `cd ~`
* `zip -g TestRequests.zip TestRequests.py`
* `aws lambda update-function-code --function-name TestRequests --zip-file fileb:///home/ec2-user/TestRequests.zip`
* Test Function (AWS Lambda Fn page)
* View result

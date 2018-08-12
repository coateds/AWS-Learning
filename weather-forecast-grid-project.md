# Weather Forecast Grid Project

With a scheduled Lambda Function, poll and retrieve weather forecast data from Open Weather Map API for sevaral locations in Washington. Present the data in an HTML table for easy comparison of that data on a web page.

## Requirements/Steps
* An s3 bucket
  * Open permissions for read from the Internet
  * Enable Static website hosting
* An IAM role for the Lambda Function
  * Lambda execution permission
  * Cloud Watch permission
  * s3 bucket permission
* A Python Lambda Function
  * Scheduled Cloud Watch trigger
  * Read from OWM API (POC needed)
    * Internet access/vpc/gateway??
  * Write a text (html) file in an s3 bucket (POC needed)
* link (in a frame) on www.davecoate.com to the s3 bucket file
  * Auto refresh on the davecoate.com page housing the link

## POC for writing a text file  --  DONE!!
* lambda_s3 role s/b sufficient
* Fn name = ForecastGridPOC
* Working result moved to file-maipulation.md

## POC for reading the OWM API
* First issue: I cannot simply `import requests`
  * Unable to import module 'lambda_function': No module named 'requests'
  * Not Used!!Start of an answer here:  https://stackoverflow.com/questions/38877058/how-do-i-add-python-libraries-to-an-aws-lambda-function-for-alexa !!Not Used
  * Not Used!!possible a better answer here:  https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html !!Not Used
  * See Instuctions in docs.aws...  next line  -->  learn to use the `zip` command in Linux
  * Even better!!/This One!!  -->  https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html

The aws python example/tutorial.
* Requires a 64-bit Amazon Linux instance
* ~/coateds.pem
* from home dir of surface:  ssh -i coateds.pem ec2-user@34.214.227.227

```
aws lambda create-function \
--region us-west-2 \
--function-name CreateThumbnail \
--zip-file fileb:///home/ec2-user/CreateThumbnail.zip \
--role arn:aws:iam::817967764457:role/service-role/lambda_s3 \
--handler CreateThumbnail.handler \
--runtime Python 3.6 \
--profile coateds \
--timeout 10 \
--memory-size 1024


aws lambda create-function \
--region us-west-2 \
--function-name TestRequests \
--zip-file fileb:///home/ec2-user/TestRequests.zip \
--role arn:aws:iam::817967764457:role/service-role/lambda_s3 \
--handler TestRequests.handler \
--runtime python3.6 \
--timeout 10 --memory-size 1024


```
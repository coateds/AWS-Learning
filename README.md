# AWS-Learning
Use notes and examples for using AWS

I am going to to all work on the Oregon region

# Attempting aws tutorial
Build a Serverless Web Application 
with AWS Lambda, Amazon API Gateway, Amazon S3, Amazon DynamoDB, and Amazon Cognito
https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/?trk=gs_card

I have configured the awscli on my Surface to use the coateds admin user in my AWS account. The key id and scret are to be placed with the rest of my passwords

## s3 bucket for static web hosting
copy source html to my s3 bucket (wildrydes-dave-coate):
`aws s3 sync s3://wildrydes-us-east-1/WebApplication/1_StaticWebHosting/website s3://wildrydes-dave-coate --region us-west-2`

When ready, the URL for the static website will be:
http://wildrydes-dave-coate.s3-website.us-west-2.amazonaws.com
After simply copying the files, the response is "The specified bucket does not have a website configuration"

Bucket policy to allow Internet access (permissions tab):
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow", 
            "Principal": "*", 
            "Action": "s3:GetObject", 
            "Resource": "arn:aws:s3:::wildrydes-dave-coate/*" 
        } 
    ] 
}
```

Enable Static website hosting (properties tab)

## Cognito
Pool Id us-west-2_SnFQ3KxEi
Pool ARN arn:aws:cognito-idp:us-west-2:817967764457:userpool/us-west-2_SnFQ3KxEi

WildRydesWebApp
App client id:  2h0qucn5c1c69lbs0lq1jd7vtl

Test: my email --> pw:H@rryBunny1

auth token = eyJraWQiOiIrVHhWTzVMakFzTHNwSmx2TFF6dUEwdW5SSGxkZ2k4QzNJUlpoQ1ZJOEs4PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJjYTI2ZTVkZi0yODQ4LTQzY2QtOTkzMS01M2VlMWQxZTIyZDAiLCJhdWQiOiIyaDBxdWNuNWMxYzY5bGJzMGxxMWpkN3Z0bCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJldmVudF9pZCI6ImM5MmQyNjhkLTlkYjktMTFlOC1iZGE1LWViNjYwMGIzNGM1MCIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTM0MDI4MTkwLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9TbkZRM0t4RWkiLCJjb2duaXRvOnVzZXJuYW1lIjoiY29hdGVkcy1hdC1vdXRsb29rLmNvbSIsImV4cCI6MTUzNDAzMTc5MCwiaWF0IjoxNTM0MDI4MTkwLCJlbWFpbCI6ImNvYXRlZHNAb3V0bG9vay5jb20ifQ.h-t0CgNKGwOCJERtOcX4BYMb8T62SDfA1fwxqmM4i7mTGvsONckDrpK0-vagTWJQU9kD-duM9llbM8s_M6Bvu61LrIHb9lp3CDmiup9FATYHJCQbPM5H7JwczOpAFbssNzcq13i5Iw1WPXxkSckXG4bvqu1viVY9ykFJcAjDCOOfIFTZTnwRyV4hHezRx-kOgxzviWdjvIEVwifyhiliZlkuFBIRrdXKMwsnWmK8UHeJTeDzeRaL9U1ieQ2QyOpZ5Ym4NT75HGoWsU4J1H51qqtLunA8AI7oeJ9THEVIhlacrsWvl3ibSjxC2N360PIlu59IjgX5voQERwoFm93Qaw

eyJraWQiOiIrVHhWTzVMakFzTHNwSmx2TFF6dUEwdW5SSGxkZ2k4QzNJUlpoQ1ZJOEs4PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJjYTI2ZTVkZi0yODQ4LTQzY2QtOTkzMS01M2VlMWQxZTIyZDAiLCJhdWQiOiIyaDBxdWNuNWMxYzY5bGJzMGxxMWpkN3Z0bCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJldmVudF9pZCI6IjlkMTVhOWI1LTlkYzktMTFlOC1iZDRjLTBiYjgwYjQ4ZGU0NiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTM0MDM0OTg4LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9TbkZRM0t4RWkiLCJjb2duaXRvOnVzZXJuYW1lIjoiY29hdGVkcy1hdC1vdXRsb29rLmNvbSIsImV4cCI6MTUzNDAzODU4OCwiaWF0IjoxNTM0MDM0OTg4LCJlbWFpbCI6ImNvYXRlZHNAb3V0bG9vay5jb20ifQ.KEbjtXWMUqQMHcThtAifwvEc8bGhZPnYxHSK8EiGE4Uk-wW_xv1Wmbopc-SHLwB43eUe0Yf5FdDwJjhACbVcxmnJvl5Z9YPw3lqaSSZqZAxFyAFnEblDxONJyNkdTkXbkH5XAVndrpw0XI86RZZDIOogclABPeksqIjIjBV03HK05_n1VfCUk26o_CVdD06k0I57NBpp2KVI4ic5wHfhSquVl4m-bNZYWpx7RHtSzfdndzDJCV4fe3FcOHioQadghiWrYYL2I1R_WghJNlGvWmnEgtWCgxAjhrGxNWaRGv6pf3fZHzCrOBKJ_gACCsZzkmIlI0HA79jHFSEZy1_q-g

## DynamoDB
arn:aws:dynamodb:us-west-2:817967764457:table/Rides

## API Gateway
Invoke URL: https://20bq7vyryf.execute-api.us-west-2.amazonaws.com/prod 
# Forecast Grid Lambda Role
* AWSLambdaBasicExecutionRole
  * Provides write permission to CloudWatch
* AWSLambdaS3ExecutionRole (customized for just one s3 Bucket?)
* AWSPosWorksCloudWatchLogs (Unnecessary?)\
* Name:  `coateds-forecast-grid-lambda-role`
* Policies
  * AWSLambdaBasicExecutionRole: AWS Managed
  * Inline
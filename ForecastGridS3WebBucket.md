# Forecast Grid S3 Web Bucket
* Name:  coateds-forcast-grid-web
* Tags:  Stack --> Forecast Grid

Bucket Policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow", 
            "Principal": "*", 
            "Action": "s3:GetObject", 
            "Resource": "[this-bucket-arn]/*" 
        } 
    ] 
}
```

Enable Static website hosting
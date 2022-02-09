# vanitynumbers_amazonconnect

The main aim of the project is to provide three best possible vanity numbers for a user phone number through amazon connect.

## Architecture Diagram

![Architecture Diagram](https://github.com/CharanZ9/vanitynumbers_amazonconnect/blob/main/documentation/architecture_diagram.png?raw=true)

## Amazon API Gateway

* vanity-number-api
  * This api gateway is exposed to accept the user phone number as a query parameter that triggers the lambda to retrieve the top three vanity numbers.
  * Base URL:
    * https://r20gf5xtd8.execute-api.us-east-1.amazonaws.com/prod
  * Methods:
    * GET()
      * Path: https://r20gf5xtd8.execute-api.us-east-1.amazonaws.com/prod/vanitynumbers
      * Description: Executes the vanity-number-lambda-function and returns the top three vanity numbers.
      * URI parameters:
        * phonenumber : query parameter
      * Sample Request:
        * https://r20gf5xtd8.execute-api.us-east-1.amazonaws.com/prod/vanitynumbers?phonenumber={user_input_phone_number}

## Amazon Connect

* ### Contact Flows

  1. Vanity Number Service Inbound Flow
  
     ![Vanity Number Service Inbound Flow](https://github.com/CharanZ9/vanitynumbers_amazonconnect/blob/main/documentation/vanity_number_service_inbound_flow.png?raw=true)
  
  2. Read Vanity Numbers Flow
  
     ![Read Vanity Numbers Flow](https://github.com/CharanZ9/vanitynumbers_amazonconnect/blob/main/documentation/read_vanity_number_service.png?raw=true)
     
## Lambda Functions

- vanity-number-lambda-function
   - Description: This function accepts the phone number as input and uses it to fetch the vanity numbers fom dynamodb.
                  If it isn't present in the db, then it creates best five vanity numbers, save those in db and return the top three from them.
                  
## DynamoDB

* ### Tables

  - vanitynumbertable
     - Stores the phone number and the corresponding vanity numbers mapping.
     - Phone number is the partition key using which items can be queried or inserted in the table
     - phoneNumber is the attribute which stores the list of five vanity numbers associated with the phone number
  
 ## AWS SAM DEPLOYMENT
  
 - The infrastructure related template and the apispec files are located at [infra](https://github.com/CharanZ9/vanitynumbers_amazonconnect/tree/main/infra)
 - I have used the following steps to deploy the application using AWS SAM.
   ```
     pip install --target ./package -r requirements.txt
   
     cd package
     zip -r ../my-deployment-package.zip .

     cd ..
     zip -g my-deployment-package.zip vanitynumber/lambda_function.py
     zip -g my-deployment-package.zip vanitynumber/__init__.py
     zip -g -r my-deployment-package.zip vanitynumber/library/

     aws s3 cp my-deployment-package.zip s3://project-vanity-numbers/zip_package/
     cd infra
     aws s3 cp api_spec.yaml s3://project-vanity-numbers/api_spec/

     sam package --template-file template.yaml --output-template-file output.yaml --s3-bucket project-vanity-numbers
     sam deploy --guided --template-file output.yaml --stack-name VanityNumbers --capabilities CAPABILITY_IAM 
   ```
 - The above steps uses the S3 bucket `project-vanity-numbers` and the stack name as `VanityNumbers`. The users has to provide their own S3 bucket and the stack name of thier choice.
 




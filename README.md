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
  
 ## AWS SAM Deployment
  
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
 
  ## Documentation
  
  Overall, I am happy with this opportunity to build this project. I sincerly thank voice foundry for providing me this opportunity. The main idea was to create a simple design that achives the functionality within the given time. I started with developing the lambda function that generates and stores the vanity numbers by the help vanity numbers library. It uses the `dictionary.txt` files to generate the meaningful vanity numbers, the idea is to include more domain related terminology into it to get better vanity numbers. This lambda will be invoked by the api gateway and the amazon connect instance. I have faced few challenges during the development of this project. Amazon connect was completly new to me and I had to refer many sources and crash courses in learning and get accustomed with this. The contact flows was only made easy to me was this youtube tutorial [here](https://www.youtube.com/playlist?list=PL4SEtvjUqihF_n-OjIsHwqqayTsAToBOx).
  
  I started with all other components i,e api gateway, lambda, sam template deployment and stack creation and first and then came to amazon connect and this turned out be a not good practice. The reason was I had everything ready with all components and amazon connect contact flows in place, but when I tried to cliam a number for testing I was facing the issue saying `You've reached the limit of Phone Numbers. To increase limit, contact support.` even though I haven't claimed any number earlier. I have contacted aws support and working to resolve the issue. I expect this to resolved today and I will update this space and also Emma Holding. 
  
  This is no way a production solutions as there are many shortcuts taken in implementing this. The validation, authentication and proper security was not in place for the api gateway and no proper staging environments for the deployment. If I had more time, I would like to change this and also a bit from the design perspective. I would have well established test cases in place, experiment with amazon Lex service and also to build a simple web app since I already have my api which returns me the top three vanity numbers. On the whole, this project provided me a great learning experience.  



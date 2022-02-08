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
  




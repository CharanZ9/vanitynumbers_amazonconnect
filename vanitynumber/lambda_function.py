import json

from botocore.exceptions import ClientError

from vanitynumber.library import wordify
import boto3


def lambda_handler(event, context):
    phone_number = ''
    print(event)
    if ("Name" in event.keys()):
        if event["Name"] == 'ContactFlowEvent':
            phone_number = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]
            if ('+44' in phone_number):
                phone_number = str(phone_number)[3:]
                vanity_number = get_vanity_number(phone_number)
                for i in range(0, len(vanity_number)):
                    vanity_number[i] = '+44' + str(vanity_number[i])
            else:
                vanity_number = get_vanity_number(phone_number)
            result_map = {"VanityNumber1": str(vanity_number[0]), "VanityNumber2": str(vanity_number[1]),
                          "VanityNumber3": str(vanity_number[2])}
            return result_map
    else:
        number = event["queryStringParameters"]['phonenumber']
        if ('+44' in number):
            number = str(number)[3:]
            vanity_number = get_vanity_number(number)
            for i in range(0, len(vanity_number)):
                vanity_number[i] = '+44' + str(vanity_number[i])
        else:
            vanity_number = get_vanity_number(number)
        result_map = {"VanityNumber1": str(vanity_number[0]), "VanityNumber2": str(vanity_number[1]),
                      "VanityNumber3": str(vanity_number[2])}
        return {
            'statusCode': 200,
            'body': json.dumps(result_map)

        }


def get_vanity_number(phone_number):
    vanity_number_from_db = get_item(phone_number)
    if ('item' in vanity_number_from_db.keys()):
        return vanity_number_from_db['item']['vanity_number']
    else:
        vanity_number = wordify.all_wordifications(phone_number)
        put_response = put_item(phone_number, vanity_number)
        return vanity_number


def put_item(phone_number, vanity_number, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('vanitynumbertable')
    response = table.put_item(
        Item={
            'phoneNumber': phone_number,
            'vanityNumber': vanity_number,
        }
    )
    return response


def get_item(phone_number, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('vanitynumbertable')

    try:
        response = table.get_item(Key={'phoneNumber': phone_number})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response
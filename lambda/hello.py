import json
import boto3


def lambda_handler(event, context):

    # create dynamodb resource object and here dynamodb is resource name
    client = boto3.resource('dynamodb')

    # this will search for dynamoDB table
    table = client.Table("testcdktable")

    if event:
        if event['httpMethod'] == 'GET' and event['path'] == '/items':
            resp = table.scan(ProjectionExpression="lastname")
            return {
                'statusCode': 200,
                'body': json.dumps(resp['Items'])
            }

        elif event['httpMethod'] == 'GET' and event['path'] == '/item':

            event['queryStringParameters']['lastname']
            try:
                response = table.get_item(
                    Key={
                        "lastname": event['queryStringParameters']['lastname']
                    }
                )
                if 'Item' in response:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(response['Item'])
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps("No data found")
                    }

            except:
                return {
                    'statusCode': 404,
                    'body': json.dumps("Error")
                }

        elif event['httpMethod'] == 'POST' and event['path'] == '/items':

            table.put_item(Item=json.loads(event['body']))
            body = {
                'Operation': 'Save',
                'Message': 'Sucess',
                'Item': json.loads(event['body'])
            }
            return {
                'statusCode': 200,
                'body': json.dumps(body)
            }

        elif event['httpMethod'] == 'DELETE' and event['path'] == '/items':

            try:

                req_body = json.loads(event['body'])

                response = table.delete_item(
                    Key={'lastname': req_body['lastname']},
                    ConditionExpression="attribute_exists (lastname)",
                    ReturnValues='ALL_OLD')
                body = {
                'Operation': 'Delete',
                'Message': 'Sucess',
                'Item': response
                }
                return {
                'statusCode': 200,
                'body': json.dumps(body)
                }
            except:
                return {
                'statusCode': 404,
                'body': json.dumps("No Record Found")
                }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps("Invalid Request")
                }

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_sns_subscriptions as subs,
    aws_dynamodb as _dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
)


class MySampleProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #create a table if not exists with given attributes
        my_table = _dynamodb.Table(self,id='dynamopTable',table_name='testcdktable',partition_key=_dynamodb.Attribute(name='lastname',type=_dynamodb.AttributeType.STRING))

        #Lambda creation 
        my_lambda= _lambda.Function(self,id='lambdaHandler',runtime=_lambda.Runtime.PYTHON_3_9,handler='hello.lambda_handler',code= _lambda.Code.from_asset('lambda')) 
       
        #create the api
        my_api = _apigateway.LambdaRestApi(self,id='lambdaapi',rest_api_name='cdkapi',handler=my_lambda)

        api_integration = _apigateway.LambdaIntegration(my_lambda)

        items = my_api.root.add_resource("items")
        items.add_method("GET", api_integration)
        items.add_method("POST", api_integration)
        items.add_method("PATCH", api_integration)
        items.add_method("DELETE", api_integration)

        item = my_api.root.add_resource("item")
        item.add_method("GET", api_integration)
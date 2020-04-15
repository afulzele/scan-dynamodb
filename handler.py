from __future__ import print_function
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def main(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('covid-global')
    result = table.scan()

    response = {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" },
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }

    while 'LastEvaluatedKey' in result:
        result = table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
        response = {
            "statusCode": 200,
            "headers": { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" },
            "body": json.dumps(result['Items'], cls=DecimalEncoder)
        }

    return response

if __name__ == "__main__":
    main('', '')
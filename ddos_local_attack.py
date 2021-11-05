import json
import urllib3


def lambda_handler(event, context):
    http = urllib3.PoolManager()
    request_num = int(event['num'])
    for i in range(request_num):
        res = http.request('GET', 'https://d3lpuqwxhx5dxu.cloudfront.net/test.html')

    response = res.data

    return {
        'statusCode': 200,
        'response': response
    }
context = ""

event = {
    "num": 5000
}
lambda_handler(event, context)

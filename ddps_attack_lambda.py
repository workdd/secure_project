import json
import urllib3


def lambda_handler(event, context):
    http = urllib3.PoolManager()

    request_count = int(event['num'])

    web_url = 'https://dv0eo9brrjhgc.cloudfront.net/web.html'

    for i in range(request_count):
        # Web request
        result = http.request('GET', web_url)

    # Response result
    response = result.data

    return {
        'statusCode': 200,
        'response': response
    }

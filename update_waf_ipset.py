import json
import boto3
import gzip

s3 = boto3.client('s3')
client = boto3.client('wafv2')
web_acl_id = 'db8df012-a599-43e0-9eb8-ee9baf872779'
ipSetName='unho-create-global-ipset'
ipSetId='99999682-dfd9-4e41-ada2-5d3237817c00'

def getLockToken():
    response = client.get_ip_set(Name=ipSetName,Scope='CLOUDFRONT',Id=ipSetId)
    return response['LockToken']

def lambda_handler(event, context):
    bucket_name = 'unho-s3'
    object_name = event['Records'][0]['s3']['object']['key']
    file_name = object_name.split("/")[1]
    file_path = '/tmp/' + file_name
    # s3 에서 로그 파일 다운로드
    s3.download_file(bucket_name, object_name, file_path)
    # s3 에서 다운로드 받은 로그 파일 압축 해제
    f = gzip.open(file_path, 'rb')
    data = str(f.read(), 'UTF-8')
    data = data.split('\n')
    data = data[2:]
    ips = [data[idx].split('\t')[4] for idx in range(len(data) - 1)]
    ip_list = set(ips)
    update_ip_list = []
    for ip in ip_list:
        cnt = ips.count(ip)
        print(f'{ip} is number of {ips.count(ip)}')
        if cnt >= 1000:
            # ip set update
            ip += '/32'
            update_ip_list.append(ip)
    response = client.update_ip_set(
                Name=ipSetName,
                Scope='CLOUDFRONT',
                Id=ipSetId,
                Description='update',
                Addresses=update_ip_list,
                LockToken=getLockToken()
            )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(update_ip_list)
    }
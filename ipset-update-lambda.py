import json
import boto3
import gzip

# Select Boto3 service
s3 = boto3.client('s3')
client = boto3.client('wafv2')

# Global variable
web_acl_id = '2d88037b-c054-4532-8dd8-39a4973c54a1'
ipSetName = 'ddos-ipset'
ipSetId = 'ae2640ce-caf4-42ae-bb98-fbe77d027513'
bucket_name = 'ddos-log-s3'

# Attacker judgment threshold hold
attacker_threshold = 1000


# get total client's ip in s3 log file
def get_total_ip(data):
    data = data.split('\n')
    data = data[2:]
    total_ip = [data[idx].split('\t')[4] for idx in range(len(data) - 1)]
    ip_set = set(total_ip)
    return total_ip, ip_set

# get locktoken for boto3
def getLockToken():
    response = client.get_ip_set(Name=ipSetName, Scope='CLOUDFRONT', Id=ipSetId)
    return response['LockToken']


def lambda_handler(event, context):
    object_name = event['Records'][0]['s3']['object']['key']
    file_name = object_name.split("/")[1]
    file_path = '/tmp/' + file_name

    # download log file in s3
    s3.download_file(bucket_name, object_name, file_path)

    # gzip file
    f = gzip.open(file_path, 'rb')

    data = str(f.read(), 'UTF-8')
    # get total client's ip in s3 log file
    total_ip, ip_set = get_total_ip(data)

    attacker_ip_list = []
    for ip in ip_set:
        cnt = total_ip.count(ip)

        # 동시 요청 수가 정의해놓은 수보다 많을 경우
        if cnt >= attacker_threshold:
            # Waf Ip set 형식으로 변경
            ip += '/32'
            # 공격자라고 판단할 ip_list에 추가함
            attacker_ip_list.append(ip)

    # update waf ip_set
    response = client.update_ip_set(
        Name=ipSetName,
        Scope='CLOUDFRONT',
        Id=ipSetId,
        Description='update',
        Addresses=attacker_ip_list,
        LockToken=getLockToken()
    )

    return {
        'statusCode': 200,
        'body': json.dumps(attacker_ip_list)
    }
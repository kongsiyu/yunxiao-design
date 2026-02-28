import requests

PAT = 'pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055'
ORG = '6385eb9c126bcb821717de64'
ID = '3f786d17c235a71122ccd9bb43'
H = {'x-yunxiao-token': PAT}

url = f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/workitems/{ID}/comments'
r = requests.get(url, headers=H, params={'page': 1, 'perPage': 3})
comments = r.json() if r.status_code == 200 else []

print('Latest 3 comments:\n')
for c in comments[:3]:
    creator = c.get('creator', {}).get('name', '?')
    content = c.get('content', '')[:200].replace('\n', ' ')
    print(f'{creator}:')
    print(f'  {content}')
    print()

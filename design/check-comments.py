import requests

PAT = 'pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055'
ORG = '6385eb9c126bcb821717de64'
ID = '3f786d17c235a71122ccd9bb43'
H = {'x-yunxiao-token': PAT}

url = f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/workitems/{ID}/comments'
r = requests.get(url, headers=H, params={'page': 1, 'perPage': 15})
comments = r.json() if r.status_code == 200 else []

print(f'Total comments: {len(comments)}')
print()
for i, c in enumerate(comments):
    creator = c.get('creator', {}).get('name', '?')
    content = c.get('content', '')[:100].replace('\n', ' ')
    ts = c.get('gmtCreate', '?')
    print(f'[{i+1}] {creator} @ {ts}: {content}')

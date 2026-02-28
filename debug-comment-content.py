import requests
import json

PAT = 'pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055'
ORG = '6385eb9c126bcb821717de64'
ID = '3f786d17c235a71122ccd9bb43'
H = {'x-yunxiao-token': PAT}

url = f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/workitems/{ID}/comments'
r = requests.get(url, headers=H, params={'page': 1, 'perPage': 5})
comments = r.json() if r.status_code == 200 else []

print('Latest comment:')
c = comments[0]
print(f'  ID: {c.get("id")}')
print(f'  Creator: {c.get("creator",{}).get("name","?")}')
print(f'  Content type: {type(c.get("content"))}')
print(f'  Content: {repr(c.get("content", "")[:300])}')
print()

# 尝试解析 htmlValue
content = c.get('content', '')
if isinstance(content, str) and 'htmlValue' in content:
    try:
        data = json.loads(content)
        print(f'  Parsed htmlValue: {data.get("htmlValue", "")[:300]}')
    except:
        print('  Failed to parse JSON')

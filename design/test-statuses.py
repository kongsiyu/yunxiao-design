import requests

PAT = 'pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055'
ORG = '6385eb9c126bcb821717de64'
PROJ = '123ac8b1bfd6691a99b64ea66d'
H = {'x-yunxiao-token': PAT}

# 尝试获取项目的所有状态
urls = [
    f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/spaces/{PROJ}/statuses',
    f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/workitem-types/Req/statuses',
    f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/projex/statuses',
]

for url in urls:
    r = requests.get(url, headers=H)
    print(f'{url[:80]}...: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, list):
            print(f'  Found {len(data)} statuses')
            for s in data[:5]:
                print(f'    - {s.get("id")}: {s.get("name")} ({s.get("nameEn")})')
        else:
            print(f'  Response: {str(data)[:200]}')
    print()

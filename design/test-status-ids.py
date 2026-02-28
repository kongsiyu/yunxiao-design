import requests

PAT = 'pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055'
ORG = '6385eb9c126bcb821717de64'
ID = '3f786d17c235a71122ccd9bb43'
H = {'x-yunxiao-token': PAT, 'Content-Type': 'application/json'}

url = f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/workitems/{ID}'

# 尝试不同的状态 ID（常见的云效状态）
status_ids = ['156603', '156604', '156605', '156606', '156607', '156608', '156609', '156610', '156611', '156612']

for sid in status_ids:
    body = {'status': {'id': sid}}
    r = requests.put(url, headers=H, json=body)
    if r.status_code == 200:
        print(f'Status {sid}: SUCCESS')
        d = r.json()
        print(f'  New status: {d.get("status",{}).get("name")} ({d.get("status",{}).get("id")})')
        # 恢复原状态
        requests.put(url, headers=H, json={'status': {'id': '156603'}})
        break
    else:
        err = r.json().get('errorMessage', '')[:50]
        print(f'Status {sid}: {r.status_code} - {err}')

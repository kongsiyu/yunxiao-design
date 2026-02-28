import requests

PAT = 'pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055'
ORG = '6385eb9c126bcb821717de64'
ID = '3f786d17c235a71122ccd9bb43'
H = {'x-yunxiao-token': PAT, 'Content-Type': 'application/json'}

# 获取当前工作项详情
url = f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/workitems/{ID}'
r = requests.get(url, headers=H)
d = r.json()

print('Current status:')
status = d.get('status', {})
print(f'  id: {status.get("id")}')
print(f'  name: {status.get("name")}')
print(f'  nameEn: {status.get("nameEn")}')
print(f'  statusStageId: {d.get("statusStageId")}')
print()

# 尝试更新状态 - 使用 stage ID
update_url = url
body = {'statusStageId': '8'}  # 尝试下一个阶段
print(f'Trying to update statusStageId to 8...')
r2 = requests.put(update_url, headers=H, json=body)
print(f'Result: {r2.status_code}')
if r2.status_code == 200:
    print('Success!')
    d2 = r2.json()
    print(f'New status: {d2.get("status",{}).get("name")}')
else:
    print(f'Error: {r2.text[:300]}')

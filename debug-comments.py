import requests
import json

PAT = 'pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055'
ORG = '6385eb9c126bcb821717de64'
ID = '3f786d17c235a71122ccd9bb43'
H = {'x-yunxiao-token': PAT}

url = f'https://openapi-rdc.aliyuncs.com/oapi/v1/projex/organizations/{ORG}/workitems/{ID}/comments'
r = requests.get(url, headers=H, params={'page': 1, 'perPage': 15})
comments = r.json() if r.status_code == 200 else []

print(f'Total comments: {len(comments)}')
print()

# 找 AI 评审评论
ai_comment = None
ai_comment_idx = -1
for i, c in enumerate(comments):
    content = c.get('content', '')
    if '[AI 评审]' in content or '[AI 设计完成]' in content:
        ai_comment = c
        ai_comment_idx = i
        print(f'Found AI comment at index {i}: {content[:50]}...')
        break

if not ai_comment:
    print('No AI comment found!')
else:
    print(f'\nAI comment index: {ai_comment_idx}')
    print(f'Comments BEFORE AI comment (new replies): {ai_comment_idx}')
    
    # 新评论是 AI 评论之前的（因为列表是倒序，最新的在前）
    new_comments = comments[:ai_comment_idx] if ai_comment_idx > 0 else []
    print(f'New comments: {len(new_comments)}')
    for c in new_comments:
        print(f'  - {c.get("creator",{}).get("name","?")}: {c.get("content","")[:60]}')

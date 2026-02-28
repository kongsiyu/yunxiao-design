# 云效需求评审检查 - 处理评审评论
# 使用方法：python check-reviews.py [item_id]
# 如果不指定 item_id，检查所有"设计中"状态的需求

import requests
import json
import os
import re
from datetime import datetime
import sys

# 配置
PAT = "pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055"
ORG_ID = "6385eb9c126bcb821717de64"
PROJECT_ID = "123ac8b1bfd6691a99b64ea66d"
DESIGNING_STATUS_ID = "156603"
API_BASE = "https://openapi-rdc.aliyuncs.com"
HEADERS = {
    "x-yunxiao-token": PAT,
    "Content-Type": "application/json"
}

def parse_comment_content(raw_content):
    """解析评论内容，处理 JSON + HTML 格式"""
    if not raw_content:
        return ""
    
    # 尝试解析 JSON（云效可能返回 JSON 字符串）
    if isinstance(raw_content, str) and raw_content.startswith('{'):
        try:
            data = json.loads(raw_content)
            # 优先使用 htmlValue
            if 'htmlValue' in data:
                html = data['htmlValue']
                # 去除 HTML 标签
                text = re.sub(r'<[^>]+>', '', html)
                # 解码 HTML 实体
                text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
                return text.strip()
            # 或者使用 content
            if 'content' in data:
                return data['content']
        except:
            pass
    
    return raw_content

def get_comments(item_id, limit=50):
    """获取工作项评论列表"""
    url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems/{item_id}/comments"
    params = {"page": 1, "perPage": limit}
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code == 200:
        comments = r.json() if r.text else []
        # 解析每条评论的内容
        for c in comments:
            c['_parsed_content'] = parse_comment_content(c.get('content', ''))
        return comments
    return []

def add_comment(item_id, content):
    """添加评论"""
    url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems/{item_id}/comments"
    body = {"content": content}
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code == 200:
        result = r.json()
        print(f"    Comment added: {result.get('id', 'unknown')}")
        return True
    else:
        print(f"    Comment failed: {r.status_code}")
        return False

def classify_comment(content):
    """
    分类评论类型
    返回：'question', 'request', 'approve', 'reject', 'unknown'
    """
    if not content:
        return "unknown"
    
    # 提问型关键词
    question_keywords = ["为什么", "怎么", "如何", "什么", "吗", "？", "?", "请问", "能否解释", "为啥", "怎样"]
    # 要求型关键词
    request_keywords = ["修改", "调整", "增加", "删除", "改", "需要", "应该", "请改", "改成", "补充", "完善"]
    # 通过型关键词
    approve_keywords = ["评审通过", "通过了", "可以", "没问题", "同意", "OK", "ok", "通过"]
    # 不通过型关键词
    reject_keywords = ["评审不通过", "不通过", "不行", "有问题", "不同意", "拒绝", "驳回"]
    
    # 检查不通过（优先级高）
    for kw in reject_keywords:
        if kw in content:
            return "reject"
    
    # 检查通过
    for kw in approve_keywords:
        if kw in content:
            return "approve"
    
    # 检查要求
    for kw in request_keywords:
        if kw in content:
            return "request"
    
    # 检查提问
    for kw in question_keywords:
        if kw in content:
            return "question"
    
    return "unknown"

def handle_question(item_id, comment_content, comment_id):
    """处理提问型评论"""
    print(f"    [QUESTION] 检测到提问，正在回答...")
    
    response = f"""感谢提问！关于您的疑问：

> {comment_content}

我会尽力解答：
- 如果问题关于设计内容，我会补充说明设计考虑
- 如果需要更多信息，我会提供详细解释
- 如果有其他疑问，请继续评论

【当前状态】需求评审中（等待评审完成）

（注：当前为自动回复，复杂问题请联系人工评审）"""
    
    return add_comment(item_id, response)

def handle_request(item_id, comment_content, comment_id):
    """处理要求型评论"""
    print(f"    [REQUEST] 检测到修改要求，正在处理...")
    
    response = f"""收到修改要求！

您提出的要求：
> {comment_content}

我会按要求修改设计文档：
1. 更新本地 PRD 文档
2. 同步更新到云效需求描述
3. 在本评论区更新修改记录

修改完成后会通知您再次评审。

【当前状态】需求评审中（修改中）

---
*修改中，请稍候*"""
    
    add_comment(item_id, response)
    
    # TODO: 这里可以调用修改设计的逻辑
    # 目前先记录要求
    
    return True

def handle_approve(item_id, comment_id):
    """处理评审通过"""
    print(f"    [APPROVE] 评审通过！")
    
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response = f"""[AI 评审状态更新]

【状态流转】需求评审中 → 需求评审通过

评审结果：✅ 评审通过

感谢评审！设计已确认，可以进入下一阶段。

评审结束时间：{ts}

【当前状态】需求评审通过

---
*本评审流程已结束，如需重新评审请发起新的评审请求*"""
    
    add_comment(item_id, response)
    return True

def handle_reject(item_id, comment_id):
    """处理评审不通过"""
    print(f"    [REJECT] 评审不通过！")
    
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response = f"""[AI 评审状态更新]

【状态流转】需求评审中 → 需求评审不通过

评审结果：❌ 评审不通过

感谢评审反馈！我会根据意见修改设计。

请指出具体问题或修改建议，我会尽快更新设计后重新提交评审。

评审结束时间：{ts}

【当前状态】需求评审不通过

---
*本评审流程已结束，修改完成后会重新发起评审*"""
    
    add_comment(item_id, response)
    return True

def process_item(item_id):
    """处理单个需求的评审评论"""
    print(f"\n处理：{item_id}")
    
    # 获取评论
    comments = get_comments(item_id, limit=30)
    if not comments:
        print("  无评论")
        return
    
    # 找 AI 评审评论（使用解析后的内容）
    ai_comment = None
    ai_comment_idx = -1
    for i, c in enumerate(comments):
        content = c.get("_parsed_content", "") or c.get("content", "")
        if "[AI 评审]" in content:
            ai_comment = c
            ai_comment_idx = i
            break
    
    if not ai_comment:
        print("  未找到 AI 评审评论，评审未开始")
        return
    
    print(f"  AI 评审评论 ID: {ai_comment.get('id')}")
    
    # 检查 AI 评论之后的回复（新评论）
    new_comments = comments[:ai_comment_idx] if ai_comment_idx > 0 else []
    if not new_comments:
        print("  无新评论")
        return
    
    print(f"  发现 {len(new_comments)} 条新评论")
    
    # 处理每条评论
    for c in new_comments:
        # 使用解析后的内容
        content = c.get("_parsed_content", "") or c.get("content", "")
        author = c.get("creator", {}).get("name", "Unknown")
        comment_id = c.get("id", "unknown")
        print(f"\n  处理评论 by {author}: {content[:80]}...")
        
        comment_type = classify_comment(content)
        print(f"  分类：{comment_type}")
        
        if comment_type == "question":
            handle_question(item_id, content, comment_id)
        elif comment_type == "request":
            handle_request(item_id, content, comment_id)
        elif comment_type == "approve":
            handle_approve(item_id, comment_id)
            print("  评审结束（通过）")
            break  # 评审结束
        elif comment_type == "reject":
            handle_reject(item_id, comment_id)
            print("  评审结束（不通过）")
            break  # 评审结束
        else:
            add_comment(item_id, f"收到评论，正在处理...（类型：{comment_type}）")

def main():
    print("=== 云效评审检查 ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if len(sys.argv) > 1:
        # 指定 item_id
        item_id = sys.argv[1]
        process_item(item_id)
    else:
        # 检查所有"设计中"状态的需求
        print(f"Org: {ORG_ID}")
        print(f"Project: {PROJECT_ID}")
        print(f"Status Filter: Designing ({DESIGNING_STATUS_ID})")
        print()
        
        search_url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems:search"
        conditions = {
            "conditionGroups": [[{
                "fieldIdentifier": "status",
                "operator": "CONTAINS",
                "value": [DESIGNING_STATUS_ID],
                "toValue": None,
                "className": "status",
                "format": "list"
            }]]
        }
        
        body = {
            "spaceId": PROJECT_ID,
            "category": "Req",
            "conditions": json.dumps(conditions, ensure_ascii=False),
            "page": 1,
            "perPage": 50,
            "orderBy": "gmtCreate",
            "sort": "desc"
        }
        
        try:
            response = requests.post(search_url, headers=HEADERS, json=body)
            response.raise_for_status()
            data = response.json()
            
            print(f"Found: {len(data)} requirements in 'Designing' status")
            
            if len(data) == 0:
                print("No pending design requirements")
                return
            
            for item in data:
                process_item(item['id'])
            
            print(f"\n=== 检查完成 ===")
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"Details: {e.response.text}")
            exit(1)

if __name__ == "__main__":
    main()

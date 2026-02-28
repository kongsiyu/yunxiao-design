# 云效需求评审流程 - 基于评论的状态机
# 使用方法：python review-flow.py <workitem_id> [action]

import requests
import json
import os
from datetime import datetime
import sys

# 配置
PAT = "pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055"
ORG_ID = "6385eb9c126bcb821717de64"
API_BASE = "https://openapi-rdc.aliyuncs.com"
HEADERS = {
    "x-yunxiao-token": PAT,
    "Content-Type": "application/json"
}

# 评审状态
REVIEW_STATES = {
    "DESIGN_DONE": "设计完成",
    "REVIEWING": "评审中",
    "APPROVED": "评审通过",
    "REJECTED": "评审不通过"
}

def get_workitem(item_id):
    """获取工作项详情"""
    url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems/{item_id}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_comments(item_id, limit=50):
    """获取工作项评论列表"""
    url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems/{item_id}/comments"
    params = {"page": 1, "perPage": limit}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json() if r.status_code == 200 else []

def add_comment(item_id, content):
    """添加评论"""
    url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems/{item_id}/comments"
    body = {"content": content}
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code == 200:
        result = r.json()
        print(f"  Comment added: {result.get('id', 'unknown')}")
        return True
    else:
        print(f"  Comment failed: {r.status_code} - {r.text[:200]}")
        return False

def get_latest_ai_comment(item_id):
    """获取最新的 AI 评审评论"""
    comments = get_comments(item_id)
    if not comments:
        return None
    
    # 找 AI 发起的评审评论（包含"[AI 评审]"标记）
    for c in reversed(comments):
        content = c.get("content", "")
        if "[AI 评审]" in content or "AI 设计完成" in content:
            return c
    return None

def classify_comment(content):
    """
    分类评论类型
    返回：'question', 'request', 'approve', 'reject', 'unknown'
    """
    if not content:
        return "unknown"
    
    # 提问型关键词
    question_keywords = ["为什么", "怎么", "如何", "什么", "吗", "？", "?", "请问", "能否解释"]
    # 要求型关键词
    request_keywords = ["修改", "调整", "增加", "删除", "改", "需要", "应该", "请改", "改成"]
    # 通过型关键词
    approve_keywords = ["评审通过", "通过了", "可以", "没问题", "同意", "OK", "ok"]
    # 不通过型关键词
    reject_keywords = ["评审不通过", "不通过", "不行", "有问题", "不同意", "拒绝"]
    
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

def handle_question(item_id, comment_content):
    """处理提问型评论"""
    print(f"  [QUESTION] 检测到提问，正在回答...")
    
    response = f"""感谢提问！关于您的疑问：

{comment_content}

我会尽力解答：
- 如果问题关于设计内容，我会补充说明设计考虑
- 如果需要更多信息，我会提供详细解释
- 如果有其他疑问，请继续评论

（注：当前为自动回复，复杂问题请联系人工评审）"""
    
    return add_comment(item_id, response)

def handle_request(item_id, comment_content):
    """处理要求型评论"""
    print(f"  [REQUEST] 检测到修改要求，正在处理...")
    
    response = f"""收到修改要求！

您提出的要求：
> {comment_content}

我会按要求修改设计文档：
1. 更新本地 PRD 文档
2. 同步更新到云效需求描述
3. 在本评论区更新修改记录

修改完成后会通知您再次评审。"""
    
    # TODO: 这里可以调用修改设计的逻辑
    # 目前先记录要求
    add_comment(item_id, response)
    
    return True

def handle_approve(item_id):
    """处理评审通过"""
    print(f"  [APPROVE] 评审通过！")
    
    response = f"""[AI 评审状态更新]

评审结果：✅ 评审通过

感谢评审！设计已确认，可以进入下一阶段。

评审结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*本评审流程已结束，如需重新评审请发起新的评审请求*"""
    
    add_comment(item_id, response)
    return True

def handle_reject(item_id):
    """处理评审不通过"""
    print(f"  [REJECT] 评审不通过！")
    
    response = f"""[AI 评审状态更新]

评审结果：❌ 评审不通过

感谢评审反馈！我会根据意见修改设计。

请指出具体问题或修改建议，我会尽快更新设计后重新提交评审。

---
*本评审流程已结束，修改完成后会重新发起评审*"""
    
    add_comment(item_id, response)
    return True

def start_review(item_id):
    """发起评审"""
    print(f"=== 发起评审 ===")
    
    item = get_workitem(item_id)
    title = item.get("subject", "Unknown")
    
    # 检查是否已有进行中的评审
    latest_comment = get_latest_ai_comment(item_id)
    if latest_comment:
        content = latest_comment.get("content", "")
        if "评审中" in content:
            print("  已有进行中的评审，请先结束当前评审")
            return False
    
    # 发起评审评论
    review_comment = f"""[AI 评审] 评审请求

需求：{title}
设计状态：设计完成
评审类型：需求评审

设计文档已生成并同步到需求描述，请评审以下内容：
1. 需求背景与目标是否准确
2. 用户故事是否完整
3. 功能设计是否合理
4. 验收标准是否可验证
5. 技术考虑是否周全

请回复评论：
- 提问型：如有疑问请提出
- 要求型：如需修改请说明
- 结束型：评审通过 / 评审不通过

---
*评审开始后，AI 会自动处理评论并更新设计*"""
    
    return add_comment(item_id, review_comment)

def check_review_status(item_id):
    """检查评审状态并处理新评论"""
    print(f"=== 检查评审状态 ===")
    
    item = get_workitem(item_id)
    title = item.get("subject", "Unknown")
    print(f"工作项：{title}")
    
    # 获取评论
    comments = get_comments(item_id, limit=20)
    if not comments:
        print("  无评论")
        return
    
    # 找 AI 评审评论
    ai_comment = None
    ai_comment_idx = -1
    for i, c in enumerate(comments):
        content = c.get("content", "")
        if "[AI 评审]" in content:
            ai_comment = c
            ai_comment_idx = i
            break
    
    if not ai_comment:
        print("  未找到 AI 评审评论，评审未开始")
        return
    
    print(f"  AI 评审评论 ID: {ai_comment.get('id')}")
    
    # 检查 AI 评论之后的回复
    new_comments = comments[:ai_comment_idx] if ai_comment_idx > 0 else []
    if not new_comments:
        print("  无新评论")
        return
    
    print(f"  发现 {len(new_comments)} 条新评论")
    
    # 处理每条评论
    for c in new_comments:
        content = c.get("content", "")
        author = c.get("creator", {}).get("name", "Unknown")
        print(f"\n  处理评论 by {author}: {content[:50]}...")
        
        comment_type = classify_comment(content)
        print(f"  分类：{comment_type}")
        
        if comment_type == "question":
            handle_question(item_id, content)
        elif comment_type == "request":
            handle_request(item_id, content)
        elif comment_type == "approve":
            handle_approve(item_id)
            break  # 评审结束
        elif comment_type == "reject":
            handle_reject(item_id)
            break  # 评审结束
        else:
            add_comment(item_id, f"收到评论，正在处理...（类型：{comment_type}）")

def complete_design(item_id):
    """完成设计，准备评审"""
    print(f"=== 完成设计 ===")
    
    item = get_workitem(item_id)
    title = item.get("subject", "Unknown")
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    comment = f"""[AI 设计完成] ({ts})

需求：{title}
状态：设计已完成，准备发起评审

设计文档已生成并同步到需求描述。

下一步：调用 start_review 发起正式评审"""
    
    return add_comment(item_id, comment)

def main():
    if len(sys.argv) < 3:
        print("用法：python review-flow.py <workitem_id> <action>")
        print("actions: complete, start, check")
        print("  complete - 完成设计")
        print("  start    - 发起评审")
        print("  check    - 检查并处理评论")
        sys.exit(1)
    
    item_id = sys.argv[1]
    action = sys.argv[2]
    
    if action == "complete":
        complete_design(item_id)
    elif action == "start":
        start_review(item_id)
    elif action == "check":
        check_review_status(item_id)
    else:
        print(f"未知 action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()

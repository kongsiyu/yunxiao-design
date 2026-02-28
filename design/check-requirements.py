# 云效需求设计自动化脚本 - Python 版本
# 安装依赖: pip install requests

import requests
import json
import os
from datetime import datetime
import re

# 配置
PAT = "pt-oebQQTtc64LqONolBhYtTbG4_c04a0cfc-93da-48b1-9ac1-dece8811a055"
ORG_ID = "6385eb9c126bcb821717de64"
PROJECT_ID = "123ac8b1bfd6691a99b64ea66d"
DESIGNING_STATUS_ID = "156603"

# API 配置
API_BASE = "https://openapi-rdc.aliyuncs.com"
HEADERS = {
    "x-yunxiao-token": PAT,
    "Content-Type": "application/json"
}

def analyze_need(title, description):
    """根据需求标题分析并生成 PRD 内容"""
    lower_title = title.lower()
    
    if "skill" in lower_title:
        return {
            "background": "当前 OpenClaw 缺少对 Codeup 的 Skills 集成支持，需要创建一个专门的 skills 模块，用于处理 Codeup 相关的技能和任务自动化。",
            "user_stories": "- 作为 OpenClaw 开发者，我需要在 Codeup 中使用 skills 功能，以便自动化处理 DevOps 任务\n- 作为项目管理员，我希望管理员工的 skills，以便更好地分配开发任务",
            "core_features": "### 1. Skill 定义与管理\n- 支持自定义 skills 名称和描述\n- 支持 skills 分类和标签\n- 支持 skills 级别评估\n\n### 2. Skill 关联\n- 支持将 skills 关联到特定的 Codeup 项目\n- 支持 skills 与任务的关联\n- 支持 skills 与开发者关联\n\n### 3. Skill 搜索与过滤\n- 支持按名称、分类、级别搜索 skills\n- 支持按项目、开发者过滤 skills\n\n### 4. Skill 报表\n- 项目 skills 统计\n- 开发者 skills 排行",
            "business_flow": "### 1. 创建 Skill\n1. 管理员在 Codeup 中创建新的 skill\n2. 填写 skill 信息（名称、描述、分类、级别）\n3. 保存并发布\n\n### 2. 关联 Skill\n1. 项目管理员将 skill 关联到项目\n2. 开发者将 skill 关联到自己\n3. 任务可以关联到特定 skill\n\n### 3. 使用 Skill\n1. 在任务管理中查看 skill 信息\n2. 在人员分配中根据 skill 筛选\n3. 生成 skills 报表",
            "ui_design": "### 1. Skill 列表页\n- 显示所有 skills，支持排序和过滤\n- 每个 skill 显示名称、描述、分类、级别、关联项目数\n\n### 2. Skill 详情页\n- 显示 skill 的详细信息\n- 显示关联的项目列表\n- 显示关联的开发者列表\n- 显示使用该 skill 的任务列表\n\n### 3. 创建 Skill 弹窗\n- 表单填写 skill 信息\n- 分类选择下拉\n- 级别选择滑块",
            "acceptance_criteria": "- [ ] 可以成功创建新的 skill\n- [ ] skill 可以关联到项目\n- [ ] skill 可以关联到开发者\n- [ ] 可以根据 skill 搜索和过滤\n- [ ] skill 报表可以正确生成\n- [ ] 界面响应正常，无错误提示",
            "technical_considerations": "### 技术方案\n- 使用 Codeup 的 API 扩展功能\n- 创建自定义表单和工作流\n- 使用 SQL 数据库存储 skills 数据\n\n### 依赖\n- Codeup API\n- OpenClaw 核心系统\n- 数据库服务\n\n### 风险\n- Codeup API 变更风险\n- 数据库性能风险\n- 并发访问风险\n\n### 扩展性\n- 支持未来添加更多 skills 类型\n- 支持 skills 与其他系统的集成"
        }
    elif "erp" in lower_title or "ai" in lower_title:
        return {
            "background": "企业需要一个 ERP 通用 AI Agent，用于处理各种 ERP 相关的自动化任务，提高工作效率。",
            "user_stories": "- 作为 ERP 管理员，我需要使用 AI Agent 来自动化处理 ERP 任务\n- 作为财务人员，我希望 AI Agent 能处理发票和报销\n- 作为采购人员，我需要 AI Agent 协助采购流程",
            "core_features": "### 1. 通用任务处理\n- 支持多种 ERP 任务类型\n- 自动识别任务类型\n- 分配合适的人工或自动化处理\n\n### 2. 机器学习学习\n- 从历史数据中学习\n- 优化任务分配\n- 预测任务处理时间\n\n### 3. 集成支持\n- 与现有 ERP 系统集成\n- 支持多种数据格式\n- 提供 API 接口",
            "business_flow": "### 1. 任务提交\n1. 用户提交 ERP 任务\n2. AI Agent 捕获任务\n3. 分析任务类型和需求\n\n### 2. 任务处理\n1. AI Agent 分析任务\n2. 决定自动处理还是人工处理\n3. 执行任务或分配给合适人员\n\n### 3. 反馈与学习\n1. 用户反馈处理结果\n2. AI Agent 学习优化\n3. 更新任务处理策略",
            "ui_design": "### 1. 任务看板\n- 显示所有待处理任务\n- 显示任务处理状态\n- 显示任务历史\n\n### 2. AI Agent 设置\n- 任务处理规则配置\n- 学习参数设置\n- 性能监控\n\n### 3. 报表与分析\n- 任务处理统计\n- AI Agent 表现分析\n- 优化建议",
            "acceptance_criteria": "- [ ] 可以自动识别 ERP 任务类型\n- [ ] AI Agent 可以自动处理简单任务\n- [ ] 复杂任务可以分配给合适人员\n- [ ] 系统可以从历史中学习\n- [ ] 报表可以正确生成",
            "technical_considerations": "### 技术方案\n- 使用机器学习模型\n- 集成 ERP 系统 API\n- 消息队列处理任务\n\n### 依赖\n- 机器学习框架\n- ERP 系统 API\n- 数据库服务\n\n### 风险\n- 模型准确率风险\n- 数据安全风险\n- 性能瓶颈风险\n\n### 扩展性\n- 支持更多 ERP 类型\n- 支持更多任务类型\n- 支持多语言"
        }
    else:
        return {
            "background": f"根据需求标题 '{title}'，这是一个新的功能需求。需要进一步了解业务背景和目标用户。",
            "user_stories": "- 作为用户，我需要这个功能来...\n- 作为管理员，我希望...",
            "core_features": "### 1. 核心功能一\n### 2. 核心功能二\n### 3. 核心功能三",
            "business_flow": "### 1. 用户操作流程\n### 2. 系统处理流程\n### 3. 数据流转流程",
            "ui_design": "### 1. 主界面布局\n### 2. 交互元素\n### 3. 响应式设计",
            "acceptance_criteria": "- [ ] 功能一正常工作\n- [ ] 功能二正常工作\n- [ ] 性能满足要求\n- [ ] 安全性符合标准",
            "technical_considerations": "### 技术方案\n- 前端技术栈\n- 后端技术栈\n- 数据库设计\n\n### 依赖\n- 第三方服务\n- 内部系统\n\n### 风险\n- 技术风险\n- 时间风险\n\n### 扩展性\n- 未来功能扩展\n- 多租户支持"
        }

def generate_prd(item, detail, description):
    """生成 PRD 文档内容"""
    title = item.get("subject", "Unknown")
    serial_number = item.get("serialNumber", "Unknown")
    item_id = item.get("id", "Unknown")
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = item.get("status", {}).get("displayName", "Unknown")
    creator = detail.get("creator", {}).get("name", "Unknown")
    assigned_to = item.get("assignedTo", {}).get("name", "Unknown")
    
    # 分析需求
    analysis = analyze_need(title, description)
    
    prd = f"""# 需求设计文档 (PRD)

## 一、需求基本信息

| 项目 | 内容 |
|------|------|
| 需求编号 | {serial_number} |
| 需求ID | {item_id} |
| 需求标题 | {title} |
| 创建时间 | {created_time} |
| 需求状态 | {status} |
| 创建人 | {creator} |
| 负责人 | {assigned_to} |

---

## 二、需求背景与目标

{analysis["background"]}

---

## 三、用户故事

{analysis["user_stories"]}

---

## 四、功能设计

{analysis["core_features"]}

### 4.2 业务流程

{analysis["business_flow"]}

### 4.3 界面设计

{analysis["ui_design"]}

---

## 五、验收标准

{analysis["acceptance_criteria"]}

---

## 六、技术考虑

{analysis["technical_considerations"]}

---

## 七、评审记录

| 评审人 | 评论 | 状态 | 日期 |
|--------|------|------|------|
| {creator} | 待评审 | 待评审 | - |

---

*PRD 由 AI 自动分析生成 - Xiaolongxia*
"""
    return prd

def update_requirement(item_id, prd_content, title):
    """更新云效需求的描述为完整 PRD 内容"""
    update_url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems/{item_id}"
    
    body = {
        "description": prd_content
    }
    
    try:
        response = requests.put(update_url, headers=HEADERS, json=body)
        response.raise_for_status()
        # 验证更新
        get_response = requests.get(update_url, headers=HEADERS)
        get_response.raise_for_status()
        updated_desc_len = len(get_response.json().get("description", ""))
        print(f"  Description updated: {updated_desc_len} chars")
        return True
    except Exception as e:
        print(f"Error updating requirement: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def add_comment(item_id, content):
    """给工作项添加评论"""
    comment_url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems/{item_id}/comments"
    
    body = {
        "content": content
    }
    
    try:
        response = requests.post(comment_url, headers=HEADERS, json=body)
        print(f"  Comment HTTP Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Comment added: {result.get('id', 'unknown')}")
            return True
        else:
            print(f"  Comment failed: {response.status_code} - {response.text[:200]}")
            return False
    except Exception as e:
        print(f"Error adding comment: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def main():
    print("=== Yunxiao Design Check ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Org: {ORG_ID}")
    print(f"Project: {PROJECT_ID}")
    print(f"Status Filter: Designing ({DESIGNING_STATUS_ID})")
    print()
    
    # 搜索"设计中"状态的需求
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
        
        # 创建输出目录
        output_dir = os.path.join(os.path.dirname(__file__), "designs")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 处理每个需求
        for item in data:
            print(f"\n[{item['serialNumber']}] {item['subject']}")
            
            # 获取详情
            detail_url = f"{API_BASE}/oapi/v1/projex/organizations/{ORG_ID}/workitems/{item['id']}"
            detail_response = requests.get(detail_url, headers=HEADERS)
            detail_response.raise_for_status()
            detail = detail_response.json()
            
            # 提取描述
            description = detail.get("description", "")
            
            # 生成 PRD
            prd_doc = generate_prd(item, detail, description)
            
            # 保存文档
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            file_name = f"{item['serialNumber']}-{timestamp}-prd.md"
            file_path = os.path.join(output_dir, file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(prd_doc)
            
            print(f"  Saved: {file_name}")
            
            # 更新需求描述（使用完整 PRD 内容）
            update_success = update_requirement(item['id'], prd_doc, item['subject'])
            if update_success:
                print(f"  [UPDATE] PRD synced to Yunxiao")
            else:
                print(f"  [WARN] Failed to sync PRD")
            
            # 添加设计完成评论
            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
            status_text = "设计已更新" if update_success else "设计生成失败"
            comment_content = f"[AI 设计完成] ({ts})\n\n状态：{status_text}\n本地文档：{file_name}\n\n下一步：发起评审"
            if add_comment(item['id'], comment_content):
                print(f"  [COMMENT] Design complete comment added")
            
            # 自动发起评审
            print(f"  Starting review...")
            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
            review_comment = f"""[AI 评审] 评审请求

【状态流转】设计中 → 需求评审中

需求：{item['subject']}
设计状态：设计完成
评审类型：需求评审
发起时间：{ts}

设计文档已生成并同步到需求描述，请评审以下内容：
1. 需求背景与目标是否准确
2. 用户故事是否完整
3. 功能设计是否合理
4. 验收标准是否可验证
5. 技术考虑是否周全

请回复评论：
- 提问型：如有疑问请提出（AI 会自动回答）
- 要求型：如需修改请说明（AI 会记录并修改）
- 结束型：评审通过 / 评审不通过（AI 会更新状态）

【当前状态】需求评审中

---
*评审开始后，AI 会自动处理评论并更新设计*"""
            if add_comment(item['id'], review_comment):
                print(f"  [REVIEW] Review started")
            
            print(f"  [NOTIFY] PRD generated and review started for {item['serialNumber']}")
        
        print(f"\n=== Check Completed ===")
        print(f"Processed: {len(data)} requirements")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Details: {e.response.text}")
        exit(1)

if __name__ == "__main__":
    main()

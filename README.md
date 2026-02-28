# 云效工作台 (Yunxiao Workspace)

> 阿里云云效 DevOps 平台对接与自动化工具集

## 项目结构

```
yunxiao/
├── README.md              # 本文件 - 云效整体说明
├── AGENTS.md              # Agent 行为指南
├── SOUL.md                # Agent 人格定义
├── USER.md                # 用户信息
├── IDENTITY.md            # 身份定义
├── TOOLS.md               # 工具配置
├── memory/                # Agent 记忆
│
├── cli/                   # 【项目 1】云效 CLI 工具
│   ├── src/               # 源代码 (Node.js)
│   ├── package.json
│   ├── README.md          # CLI 使用文档
│   └── SKILL.md           # OpenClaw Skill 定义
│
└── design/                # 【项目 2】自动化脚本与设计
    ├── *.py               # Python 自动化脚本
    ├── *.ps1              # PowerShell 辅助脚本
    ├── designs/           # 生成的设计文档 (PRD)
    ├── memory/            # design 子项目记忆
    └── README.md          # design 项目说明
```

---

## 快速开始

### CLI 工具

```bash
cd cli
npm install
npm link          # 全局安装 yunxiao 命令
yunxiao --help    # 查看可用命令
```

详见：[cli/README.md](cli/README.md)

### 自动化脚本

```bash
cd design
python yunxiao_config.py    # 配置向导
python check-requirements.py  # 检查需求
python review-flow.py        # 评审流程
```

详见：[design/README.md](design/README.md)

---

## 云效 API 基础

**基础 URL:** `https://openapi-rdc.aliyuncs.com`

**认证方式:** Personal Access Token (PAT)

**获取 PAT:** https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token

**核心接口:**

| 功能 | Method | 路径 |
|------|--------|------|
| 项目搜索 | POST | `/oapi/v1/projex/organizations/{orgId}/projects:search` |
| 工作项搜索 | POST | `/oapi/v1/projex/organizations/{orgId}/workitems:search` |
| 创建工作项 | POST | `/oapi/v1/projex/organizations/{orgId}/workitems` |
| 添加评论 | POST | `/oapi/v1/projex/organizations/{orgId}/workitems/{id}/comments` |

---

## 相关资源

- [云效 API 文档](https://help.aliyun.com/zh/yunxiao/developer-reference/)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [GitHub 仓库](https://github.com/kongsiyu/yunxiao-design)

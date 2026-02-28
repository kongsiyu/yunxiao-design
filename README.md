# 云效自动化工具集 (Yunxiao Automation)

> 云效 CLI 工具 + OpenClaw Agent 集成

## ?? 项目结构

``
yunxiao/
├── cli/                    # 云效 CLI 工具 (Node.js)
│   ├── src/               # 源代码
│   ├── package.json       # 依赖配置
│   ├── SKILL.md           # 技能说明
│   └── README.md          # CLI 使用文档
│
├── agent/                 # OpenClaw Agent 配置
│   ├── AGENTS.md          # Agent 行为指南
│   ├── SOUL.md            # Agent 人格定义
│   ├── USER.md            # 用户信息
│   └── ...                # 其他配置文件
│
├── designs/               # 生成的设计文档
├── check-requirements.py  # 需求检查脚本
├── check-reviews.py       # 评审检查脚本
├── review-flow.py         # 评审流程脚本
├── yunxiao_config.py      # 交互式配置工具
└── README.md              # 本文件
``

---

## ??? CLI 工具

云效命令行工具，提供类似 \gh auth\ 的交互式配置体验。

### 安装
\\\ash
cd cli
npm install
\\\

### 配置
\\\ash
# 交互式配置（推荐）
python ../yunxiao_config.py

# 或手动设置环境变量
\ = "pt-xxxxx"
\ = "devops.aliyun.com"
\ = "xxxxx"
\\\

### 功能
- ?? 交互式认证配置
- ?? 组织选择与管理
- ?? 需求/工作项管理
- ?? 评审流程自动化

详见：[cli/README.md](cli/README.md)

---

## ?? OpenClaw Agent

基于 OpenClaw 的智能助手，自动化处理云效需求。

### 当前功能

#### 自动检查"设计中"需求
\\\ash
python check-requirements.py
\\\

详见原有 README 内容...

---

## ?? 相关链接

- [云效 API 文档](https://help.aliyun.com/zh/yunxiao/developer-reference/)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [GitHub 仓库](https://github.com/kongsiyu/yunxiao-design)

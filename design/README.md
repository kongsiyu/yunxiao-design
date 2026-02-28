# 云效自动化设计 (Yunxiao Design)

> 云效工作项自动化处理与设计文档生成

## 目录结构

```
design/
├── README.md              # 本文件
├── yunxiao_config.py      # 配置向导（运行一次）
│
├── check-requirements.py  # 检查工作项需求
├── check-reviews.py       # 检查评审状态
├── review-flow.py         # 评审流程自动化
│
├── designs/               # 生成的设计文档 (PRD)
│   └── GJBL-*.md
│
└── memory/                # 子项目记忆
```

## 配置

首次运行前执行：

```bash
python yunxiao_config.py
```

会提示输入：
- `YUNXIAO_PAT` - 云效个人访问令牌
- `YUNXIAO_ORG_ID` - 组织 ID
- `YUNXIAO_PROJECT_ID` - 默认项目 ID

配置会保存到 `.env.ps1` 文件。

## 主要脚本

### `check-requirements.py`
检查工作项的需求完整性，生成待办清单。

### `check-reviews.py`
检查评审状态，列出待评审项。

### `review-flow.py`
自动化评审流程，包括状态更新和评论。

## 设计文档

`designs/` 目录存放自动生成的 PRD 文档，命名格式：
```
GJBL-{序号}-{YYYYMMDD}-{HHMMSS}-prd.md
```

---

**返回主目录:** [../README.md](../README.md)

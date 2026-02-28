# TOOLS.md - 云效开发环境配置

## 云效认证配置

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `YUNXIAO_PAT` | ✅ | 云效个人访问令牌 |
| `YUNXIAO_ORG_ID` | ✅ | 组织 ID |
| `YUNXIAO_PROJECT_ID` | 可选 | 默认项目 ID |
| `YUNXIAO_USER_ID` | 可选 | 当前用户 ID |

### 配置位置

- **CLI 项目** (`cli/`): 从系统环境变量读取
- **Design 项目** (`design/`): 从 `design/.env.ps1` 读取

### 获取 PAT

https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token

---

## 本地开发

### CLI 调试
```bash
cd cli
node src/index.js [command]
```

### Design 脚本调试
```bash
cd design
python yunxiao_config.py  # 配置向导
python check-requirements.py
```

---

## 相关资源

- [云效 API 文档](https://help.aliyun.com/zh/yunxiao/developer-reference/)
- [OpenClaw 文档](https://docs.openclaw.ai)

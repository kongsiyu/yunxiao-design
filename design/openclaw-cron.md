# OpenClaw Cron 配置

## 定时任务

### 1. 检查需求 + 生成 PRD + 发起评审（每 5 分钟）

```json
{
  "name": "yunxiao-check-requirements",
  "schedule": "*/5 * * * *",
  "command": ["python", "C:\\Users\\boil\\.openclaw\\workspace\\yunxiao-design\\check-requirements.py"],
  "workdir": "C:\\Users\\boil\\.openclaw\\workspace\\yunxiao-design",
  "enabled": true
}
```

### 2. 检查评审评论（每 2 分钟）

```json
{
  "name": "yunxiao-check-reviews",
  "schedule": "*/2 * * * *",
  "command": ["python", "C:\\Users\\boil\\.openclaw\\workspace\\yunxiao-design\\check-reviews.py"],
  "workdir": "C:\\Users\\boil\\.openclaw\\workspace\\yunxiao-design",
  "enabled": true
}
```

## 配置方法

在 OpenClaw 配置文件中添加 cron 任务，或通过命令：

```bash
openclaw cron add --name yunxiao-check-requirements --schedule "*/5 * * * *" --command "python C:\Users\boil\.openclaw\workspace\yunxiao-design\check-requirements.py"
openclaw cron add --name yunxiao-check-reviews --schedule "*/2 * * * *" --command "python C:\Users\boil\.openclaw\workspace\yunxiao-design\check-reviews.py"
```

## 管理命令

```bash
# 查看 cron 任务
openclaw cron list

# 启用/禁用
openclaw cron enable yunxiao-check-requirements
openclaw cron disable yunxiao-check-requirements

# 删除
openclaw cron remove yunxiao-check-requirements

# 手动触发
openclaw cron run yunxiao-check-requirements
```

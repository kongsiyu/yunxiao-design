# 云效需求设计自动化 - ✅ 已完成

## ✅ 当前功能

### 自动检查"设计中"需求
```bash
python check-requirements.py
```

输出示例：
```
=== Yunxiao Design Check ===
Time: 2026-02-25 15:50:48
Org: 6385eb9c126bcb821717de64
Project: 123ac8b1bfd6691a99b64ea66d
Status Filter: Designing (156603)

Found: 1 requirements in 'Designing' status

[GJBL-1] 为 openclaw 添加一个 codeup 的 skills
  Saved: GJBL-1-20260225-155049-prd.md
  Description updated: 1706 chars
  [NOTIFY] PRD generated and synced for GJBL-1

=== Check Completed ===
Processed: 1 requirements
```

### 工作流程
1. **检查云效** - 获取状态为"设计中"的需求
2. **AI 分析** - 根据需求标题和描述生成完整 PRD
3. **保存本地** - 设计文档保存到 `designs/` 目录
4. **同步云效** - 将 PRD 内容更新到云效需求描述字段

### 设计文档模板
- 需求基本信息（编号、ID、标题、状态、负责人等）
- 背景与目标
- 用户故事
- 功能设计（核心功能、业务流程、界面设计）
- 验收标准
- 技术考虑
- 评审记录

## ⏳ 待完善功能

1. **定时任务** - 每 5 分钟自动运行（cron/Windows 任务计划）
2. **附件上传** - 云效 API 不支持（已放弃）
3. **评审人通知** - 云效 API 不支持（已放弃）

## 📁 项目结构
```
yunxiao-design/
├── .env.ps1              # API 配置（敏感信息）
├── check-requirements.py # 主脚本（Python）
├── check-requirements.ps1 # 主脚本（PowerShell，备用）
├── cron-config.md        # 定时任务配置指南
├── design-logic.md       # 设计逻辑说明
├── README.md             # 项目说明
└── designs/              # 生成的设计文档
```

## 🚀 设置定时任务

### Windows 任务计划程序
```powershell
# 以管理员身份运行 PowerShell

$taskName = "YunxiaoDesignCheck"
$scriptPath = "C:\Users\boil\.openclaw\workspace\yunxiao-design\check-requirements.py"
$pythonExe = "python"

$action = New-ScheduledTaskAction -Execute $pythonExe -Argument "`"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration ([TimeSpan]::MaxValue)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Highest

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Description "云效需求设计自动化检查"
```

### 管理命令
```powershell
# 查看任务
Get-ScheduledTask -TaskName "YunxiaoDesignCheck"

# 手动触发测试
Start-ScheduledTask -TaskName "YunxiaoDesignCheck"

# 查看运行历史
Get-ScheduledTaskInfo -TaskName "YunxiaoDesignCheck"

# 删除任务
Unregister-ScheduledTask -TaskName "YunxiaoDesignCheck" -Confirm:$false
```

## 📊 测试结果
- ✅ API 调用正常
- ✅ 状态过滤正常（Designing: 156603）
- ✅ 需求列表获取正常
- ✅ 需求详情获取正常
- ✅ 设计文档生成正常
- ✅ 云效描述更新正常

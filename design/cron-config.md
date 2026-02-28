# 定时任务配置

## Windows 任务计划程序

### 创建任务
```powershell
# 以管理员身份运行 PowerShell 执行以下命令

$taskName = "YunxiaoDesignCheck"
$scriptPath = "C:\Users\boil\.openclaw\workspace\yunxiao-design\check-requirements.ps1"
$triggerTime = (New-TimeSpan -Minutes 5)

# 创建每 5 分钟执行的任务
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval $triggerTime -RepetitionDuration ([TimeSpan]::MaxValue)
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

## 环境变量设置

在系统环境变量中添加：
- **YUNXIAO_PAT**: 你的云效 Personal Access Token

或者在脚本执行前手动设置：
```powershell
$env:YUNXIAO_PAT = "your-token-here"
```

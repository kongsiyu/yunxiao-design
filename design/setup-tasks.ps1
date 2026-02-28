# 云效定时任务配置脚本
# 以管理员身份运行 PowerShell 执行此脚本

# 获取 Python 路径
$pythonExe = "python"

# 脚本路径
$checkReqScript = "C:\Users\boil\.openclaw\workspace\yunxiao-design\check-requirements.py"
$checkReviewsScript = "C:\Users\boil\.openclaw\workspace\yunxiao-design\check-reviews.py"

# 任务名称
$taskNameReq = "YunxiaoCheckRequirements"
$taskNameReviews = "YunxiaoCheckReviews"

Write-Host "=== 配置云效定时任务 ===" -ForegroundColor Cyan

# 检查是否管理员
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: 请以管理员身份运行此脚本" -ForegroundColor Red
    Write-Host "右键 PowerShell -> 以管理员身份运行" -ForegroundColor Yellow
    exit 1
}

# 删除旧任务（如果存在）
Write-Host "`n1. 清理旧任务..." -ForegroundColor Yellow
try {
    Unregister-ScheduledTask -TaskName $taskNameReq -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "  已删除：$taskNameReq" -ForegroundColor Gray
} catch {}

try {
    Unregister-ScheduledTask -TaskName $taskNameReviews -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "  已删除：$taskNameReviews" -ForegroundColor Gray
} catch {}

# 创建检查需求任务（每 5 分钟）
Write-Host "`n2. 创建检查需求任务（每 5 分钟）..." -ForegroundColor Yellow
$actionReq = New-ScheduledTaskAction -Execute $pythonExe -Argument "`"$checkReqScript`""
$triggerReq = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration ([TimeSpan]::MaxValue)
$principalReq = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Highest
Register-ScheduledTask -TaskName $taskNameReq -Action $actionReq -Trigger $triggerReq -Principal $principalReq -Description "云效需求检查 - 每 5 分钟运行" | Out-Null
Write-Host "  已创建：$taskNameReq" -ForegroundColor Green

# 创建检查评审任务（每 2 分钟）
Write-Host "`n3. 创建检查评审任务（每 2 分钟）..." -ForegroundColor Yellow
$actionReviews = New-ScheduledTaskAction -Execute $pythonExe -Argument "`"$checkReviewsScript`""
$triggerReviews = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 2) -RepetitionDuration ([TimeSpan]::MaxValue)
$principalReviews = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Highest
Register-ScheduledTask -TaskName $taskNameReviews -Action $actionReviews -Trigger $triggerReviews -Principal $principalReviews -Description "云效评审检查 - 每 2 分钟运行" | Out-Null
Write-Host "  已创建：$taskNameReviews" -ForegroundColor Green

Write-Host "`n=== 配置完成 ===" -ForegroundColor Cyan
Write-Host "`n管理命令:" -ForegroundColor White
Write-Host "  查看任务：Get-ScheduledTask -TaskName `"Yunxiao*`"" -ForegroundColor Gray
Write-Host "  手动触发：Start-ScheduledTask -TaskName `"$taskNameReq`"" -ForegroundColor Gray
Write-Host "  查看历史：Get-ScheduledTaskInfo -TaskName `"$taskNameReq`"" -ForegroundColor Gray
Write-Host "  删除任务：Unregister-ScheduledTask -TaskName `"$taskNameReq`" -Confirm:`$false" -ForegroundColor Gray

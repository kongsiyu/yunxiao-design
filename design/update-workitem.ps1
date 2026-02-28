# 云效需求更新脚本 - 测试用
# 功能：更新需求描述、上传附件

param(
    [string]$ItemId = "3f786d17c235a71122ccd9bb43",
    [string]$PrdFilePath = ""
)

# 加载配置
& "$PSScriptRoot\.env.ps1"
$Pat = $env:YUNXIAO_PAT
$OrgId = $env:YUNXIAO_ORG_ID

if ([string]::IsNullOrEmpty($Pat) -or [string]::IsNullOrEmpty($OrgId)) {
    Write-Host "Error: PAT or OrgID not configured" -ForegroundColor Red
    exit 1
}

$ApiBase = "https://openapi-rdc.aliyuncs.com"
$Headers = @{
    "x-yunxiao-token" = $Pat
    "Content-Type" = "application/json"
}

Write-Host "=== Yunxiao Update Test ===" -ForegroundColor Cyan
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "Org: $OrgId"
Write-Host "WorkItem ID: $ItemId`n"

# 1. 先获取当前需求详情
$DetailUrl = "$ApiBase/oapi/v1/projex/organizations/$OrgId/workitems/$ItemId"
try {
    $detail = Invoke-RestMethod -Uri $DetailUrl -Method Get -Headers $Headers
    Write-Host "Current Title: $($detail.subject)" -ForegroundColor Green
    Write-Host "Current Description Length: $($detail.description.Length) chars`n"
} catch {
    Write-Host "Error getting workitem: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2. 准备更新内容（从 PRD 提取）
if ([string]::IsNullOrEmpty($PrdFilePath)) {
    $designsDir = "$PSScriptRoot\designs"
    $latestPrd = Get-ChildItem -Path $designsDir -Filter "*-prd.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestPrd) {
        $PrdFilePath = $latestPrd.FullName
        Write-Host "Using latest PRD: $PrdFilePath`n" -ForegroundColor Gray
    } else {
        Write-Host "No PRD file found" -ForegroundColor Yellow
        exit 1
    }
}

# 读取 PRD 内容
$prdContent = Get-Content -Path $PrdFilePath -Raw -Encoding UTF8
Write-Host "PRD Content Length: $($prdContent.Length) chars`n" -ForegroundColor Gray

# 简单提取：取整个 PRD 内容作为描述
$newDescription = $prdContent

Write-Host "=== Updating WorkItem Description ===" -ForegroundColor Yellow

# 3. 更新需求描述
$updateBody = @{
    description = $newDescription
} | ConvertTo-Json -Depth 5 -Compress

try {
    $updateResponse = Invoke-RestMethod -Uri $DetailUrl -Method Put -Headers $Headers -Body $updateBody
    Write-Host "Description updated successfully!" -ForegroundColor Green
    Write-Host "New Description Length: $($updateResponse.description.Length) chars`n"
} catch {
    Write-Host "Error updating description: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Yellow
    }
}

# 4. 上传 PRD 作为附件
Write-Host "=== Uploading PRD as Attachment ===" -ForegroundColor Yellow

$uploadUrl = "$ApiBase/oapi/v1/projex/organizations/$OrgId/attachments"

# 读取文件为 Base64
$prdBytes = [System.IO.File]::ReadAllBytes($PrdFilePath)
$prdBase64 = [System.Convert]::ToBase64String($prdBytes)
$fileName = Split-Path -Path $PrdFilePath -Leaf

$uploadBody = @{
    fileName = $fileName
    fileSize = $prdBytes.Length
    fileData = $prdBase64
    workItemId = $ItemId
} | ConvertTo-Json -Depth 5

try {
    $uploadResponse = Invoke-RestMethod -Uri $uploadUrl -Method Post -Headers $Headers -Body $uploadBody
    Write-Host "Attachment uploaded successfully!" -ForegroundColor Green
    Write-Host "Attachment ID: $($uploadResponse.id)" -ForegroundColor Gray
    Write-Host "File Name: $($uploadResponse.fileName)" -ForegroundColor Gray
} catch {
    Write-Host "Error uploading attachment: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Yellow
    }
}

Write-Host "`n=== Update Test Completed ===" -ForegroundColor Cyan

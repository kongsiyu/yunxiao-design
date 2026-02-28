$envPath = "C:\Users\boil\.openclaw\workspace\yunxiao-design\.env.ps1"
if (Test-Path $envPath) { & $envPath }
$Pat = $env:YUNXIAO_PAT
$ApiBase = "https://openapi-rdc.aliyuncs.com"
$ProjectId = "123ac8b1bfd6691a99b64ea66d"
$Headers = @{ "Authorization" = "Bearer $Pat"; "Content-Type" = "application/json" }
$WorkItemsUrl = "$ApiBase/api/v1/projects/$ProjectId/work_items"
$response = Invoke-RestMethod -Uri $WorkItemsUrl -Method Get -Headers $Headers
$response | ConvertTo-Json -Depth 10

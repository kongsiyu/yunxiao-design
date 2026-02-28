& "$PSScriptRoot\.env.ps1"
$Pat = $env:YUNXIAO_PAT
$OrgId = $env:YUNXIAO_ORG_ID
$ItemId = "3f786d17c235a71122ccd9bb43"

$ApiBase = "https://openapi-rdc.aliyuncs.com"
$Headers = @{ "x-yunxiao-token" = $Pat }

$DetailUrl = "$ApiBase/oapi/v1/projex/organizations/$OrgId/workitems/$ItemId"
$detail = Invoke-RestMethod -Uri $DetailUrl -Method Get -Headers $Headers

Write-Host "=== Full Response ===" -ForegroundColor Cyan
$detail | ConvertTo-Json -Depth 10

Write-Host "`n=== Description Field ===" -ForegroundColor Cyan
Write-Host "description: '$($detail.description)'"

Write-Host "`n=== Custom Fields ===" -ForegroundColor Cyan
if ($detail.customFieldValues) {
    foreach ($f in $detail.customFieldValues) {
        Write-Host "Field: $($f.fieldName) ($($f.fieldId))"
        if ($f.values) {
            foreach ($v in $f.values) {
                Write-Host "  Value: $($v.displayValue)"
            }
        }
    }
} else {
    Write-Host "No customFieldValues"
}

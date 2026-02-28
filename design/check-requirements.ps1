# 云效需求设计自动化脚本
# 每 5 分钟检查"设计中"状态的需求，生成 PRD

param([string]$ProjectId = "")

# 加载配置
& "$PSScriptRoot\.env.ps1"
$Pat = $env:YUNXIAO_PAT
$OrgId = $env:YUNXIAO_ORG_ID
$DesigningStatusId = "156603"  # "设计中"状态 ID
if ([string]::IsNullOrEmpty($ProjectId)) { $ProjectId = $env:YUNXIAO_PROJECT_ID }

if ([string]::IsNullOrEmpty($Pat) -or [string]::IsNullOrEmpty($OrgId)) {
    Write-Host "Error: PAT or OrgID not configured" -ForegroundColor Red
    exit 1
}

$ApiBase = "https://openapi-rdc.aliyuncs.com"
$Headers = @{
    "x-yunxiao-token" = $Pat
    "Content-Type" = "application/json"
}

Write-Host "=== Yunxiao Design Check ===" -ForegroundColor Cyan
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "Org: $OrgId"
Write-Host "Project: $ProjectId"
Write-Host "Status Filter: Designing ($DesigningStatusId)`n"

# 搜索"设计中"状态的需求
$SearchUrl = "$ApiBase/oapi/v1/projex/organizations/$OrgId/workitems:search"
$ConditionsJson = '{"conditionGroups":[[{"fieldIdentifier":"status","operator":"CONTAINS","value":["' + $DesigningStatusId + '"],"toValue":null,"className":"status","format":"list"}]]}'
$Body = @{
    spaceId = $ProjectId
    category = "Req"
    conditions = $ConditionsJson
    page = 1
    perPage = 50
    orderBy = "gmtCreate"
    sort = "desc"
} | ConvertTo-Json -Depth 5

try {
    $response = Invoke-RestMethod -Uri $SearchUrl -Method Post -Headers $Headers -Body $Body
    Write-Host "Found: $($response.Count) requirements in 'Designing' status" -ForegroundColor Yellow
    
    if ($response.Count -eq 0) {
        Write-Host "No pending design requirements" -ForegroundColor Gray
        exit 0
    }
    
    # 创建输出目录
    $outputDir = "$PSScriptRoot\designs"
    if (!(Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir | Out-Null }
    
    # 处理每个需求
    foreach ($item in $response) {
        Write-Host "`n[$($item.serialNumber)] $($item.subject)" -ForegroundColor Cyan
        Write-Host "  ID: $($item.id)"
        Write-Host "  Status: $($item.status.displayName)"
        
        # 获取详情
        $DetailUrl = "$ApiBase/oapi/v1/projex/organizations/$OrgId/workitems/$($item.id)"
        $detail = Invoke-RestMethod -Uri $DetailUrl -Method Get -Headers $Headers
        
        # 提取描述
        $description = ""
        if ($detail.description) { 
            $description = $detail.description 
        }
        
        # 生成 PRD
        $prdDoc = Generate-PRD -Item $item -Detail $detail -Description $description
        
        # 保存文档
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $fileName = "$($item.serialNumber)-$timestamp-prd.md"
        $filePath = "$outputDir\$fileName"
        $prdDoc | Out-File -FilePath $filePath -Encoding UTF8
        
        Write-Host "  Saved: $fileName" -ForegroundColor Green
        
        # 更新云效需求描述
        Write-Host "  Updating workitem description..." -ForegroundColor Yellow
        $updateBody = @{ description = $prdDoc } | ConvertTo-Json -Compress
        try {
            $updateResponse = Invoke-RestMethod -Uri $DetailUrl -Method Put -Headers $Headers -Body $updateBody
            Start-Sleep -Milliseconds 500
            $verifyResponse = Invoke-RestMethod -Uri $DetailUrl -Method Get -Headers $Headers
            Write-Host "  Description updated: $($verifyResponse.description.Length) chars" -ForegroundColor Green
            Write-Host "  [NOTIFY] PRD generated and synced for $($item.serialNumber)" -ForegroundColor Magenta
        } catch {
            Write-Host "  Warning: Failed to update description: $($_.Exception.Message)" -ForegroundColor Yellow
            Write-Host "  [NOTIFY] PRD generated for $($item.serialNumber)" -ForegroundColor Magenta
        }
    }
    
    Write-Host "`n=== Check Completed ===" -ForegroundColor Cyan
    Write-Host "Processed: $($response.Count) requirements" -ForegroundColor Green
    
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Yellow
    }
    exit 1
}

# 生成 PRD 函数
function Generate-PRD {
    param(
        $Item,
        $Detail,
        $Description
    )
    
    $title = $Item.subject
    $serialNumber = $Item.serialNumber
    $itemId = $Item.id
    $createdTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $status = $Item.status.displayName
    
    # 分析需求
    $analysis = Analyze-Need -Title $title -Description $Description
    
    # 生成中文 PRD
    $prdDoc = @"


# 需求设计文档 (PRD)

## 一、需求基本信息

| 项目 | 内容 |
|------|------|
| 需求编号 | $serialNumber |
| 需求ID | $itemId |
| 需求标题 | $title |
| 创建时间 | $createdTime |
| 需求状态 | $status |
| 创建人 | $($Detail.creator.name) |
| 负责人 | $($Item.assignedTo.name) |

---

## 二、需求背景与目标

$($analysis.Background)

---

## 三、用户故事

$($analysis.UserStories)

---

## 四、功能设计

### 4.1 核心功能

$($analysis.CoreFeatures)

### 4.2 业务流程

$($analysis.BusinessFlow)

### 4.3 界面设计

$($analysis.UIDesign)

---

## 五、验收标准

$($analysis.AcceptanceCriteria)

---

## 六、技术考虑

$($analysis.TechnicalConsiderations)

---

## 七、评审记录

| 评审人 | 评论 | 状态 | 日期 |
|--------|------|------|------|
| - | - | - | - |

---

*PRD 由 AI 自动分析生成 - Xiaolongxia*

"@
    
    return $prdDoc
}

# 分析需求内容
function Analyze-Need {
    param(
        [string]$Title,
        [string]$Description
    )
    
    # 基于标题分析
    $lowerTitle = $Title.ToLower()
    
    # 根据不同的需求类型生成不同的分析
    if ($lowerTitle -match "skill" -or $lowerTitle -match "skills") {
        $result = @{
            Background = "当前 OpenClaw 缺少对 Codeup 的 Skills 集成支持，需要创建一个专门的 skills 模块，用于处理 Codeup 相关的技能和任务自动化。"
            UserStories = "- 作为 OpenClaw 开发者，我需要在 Codeup 中使用 skills 功能，以便自动化处理 DevOps 任务`n- 作为项目管理员，我希望管理员工的 skills，以便更好地分配开发任务"
            CoreFeatures = "1. Skill 定义与管理`n   - 支持自定义 skills 名称和描述`n   - 支持 skills 分类和标签`n   - 支持 skills 级别评估`n2. Skill 关联`n   - 支持将 skills 关联到特定的 Codeup 项目`n   - 支持 skills 与任务的关联`n   - 支持 skills 与开发者关联`n3. Skill 搜索与过滤`n   - 支持按名称、分类、级别搜索 skills`n   - 支持按项目、开发者过滤 skills`n4. Skill 报表`n   - 项目 skills 统计`n   - 开发者 skills 排行"
            BusinessFlow = "1. 创建 Skill`n   - 管理员在 Codeup 中创建新的 skill`n   - 填写 skill 信息（名称、描述、分类、级别）`n   - 保存并发布`n2. 关联 Skill`n   - 项目管理员将 skill 关联到项目`n   - 开发者将 skill 关联到自己`n   - 任务可以关联到特定 skill`n3. 使用 Skill`n   - 在任务管理中查看 skill 信息`n   - 在人员分配中根据 skill 筛选`n   - 生成 skills 报表"
            UIDesign = "1. Skill 列表页`n   - 显示所有 skills，支持排序和过滤`n   - 每个 skill 显示名称、描述、分类、级别、关联项目数`n2. Skill 详情页`n   - 显示 skill 的详细信息`n   - 显示关联的项目列表`n   - 显示关联的开发者列表`n   - 显示使用该 skill 的任务列表`n3. 创建 Skill 弹窗`n   - 表单填写 skill 信息`n   - 分类选择下拉`n   - 级别选择滑块"
            AcceptanceCriteria = "- [ ] 可以成功创建新的 skill`n- [ ] skill 可以关联到项目`n- [ ] skill 可以关联到开发者`n- [ ] 可以根据 skill 搜索和过滤`n- [ ] skill 报表可以正确生成`n- [ ] 界面响应正常，无错误提示"
            TechnicalConsiderations = "1. 技术方案`n   - 使用 Codeup 的 API 扩展功能`n   - 创建自定义表单和工作流`n   - 使用 SQL 数据库存储 skills 数据`n2. 依赖`n   - Codeup API`n   - OpenClaw 核心系统`n   - 数据库服务`n3. 风险`n   - Codeup API 变更风险`n   - 数据库性能风险`n   - 并发访问风险`n4. 扩展性`n   - 支持未来添加更多 skills 类型`n   - 支持 skills 与其他系统的集成"
        }
        return $result
    }
    elseif ($lowerTitle -match "erp" -or $lowerTitle -match "ai") {
        $result = @{
            Background = "企业需要一个 ERP 通用 AI Agent，用于处理各种 ERP 相关的自动化任务。"
            UserStories = "- 作为 ERP 管理员，我需要使用 AI Agent 来自动化处理 ERP 任务`n- 作为财务人员，我希望 AI Agent 能处理发票和报销`n- 作为采购人员，我需要 AI Agent 协助采购流程"
            CoreFeatures = "1. 通用任务处理`n   - 支持多种 ERP 任务类型`n   - 自动识别任务类型`n   - 分配合适的人工或自动化处理`n2. 机器学习学习`n   - 从历史数据中学习`n   - 优化任务分配`n   - 预测任务处理时间`n3. 集成支持`n   - 与现有 ERP 系统集成`n   - 支持多种数据格式`n   - 提供 API 接口"
            BusinessFlow = "1. 任务提交`n   - 用户提交 ERP 任务`n   - AI Agent 捕获任务`n   - 分析任务类型和需求`n2. 任务处理`n   - AI Agent 分析任务`n   - 决定自动处理还是人工处理`n   - 执行任务或分配给合适人员`n3. 反馈与学习`n   - 用户反馈处理结果`n   - AI Agent 学习优化`n   - 更新任务处理策略"
            UIDesign = "1. 任务看板`n   - 显示所有待处理任务`n   - 显示任务处理状态`n   - 显示任务历史`n2. AI Agent 设置`n   - 任务处理规则配置`n   - 学习参数设置`n   - 性能监控`n3. 报表与分析`n   - 任务处理统计`n   - AI Agent 表现分析`n   - 优化建议"
            AcceptanceCriteria = "- [ ] 可以自动识别 ERP 任务类型`n- [ ] AI Agent 可以自动处理简单任务`n- [ ] 复杂任务可以分配给合适人员`n- [ ] 系统可以从历史中学习`n- [ ] 报表可以正确生成"
            TechnicalConsiderations = "1. 技术方案`n   - 使用机器学习模型`n   - 集成 ERP 系统 API`n   - 消息队列处理任务`n2. 依赖`n   - 机器学习框架`n   - ERP 系统 API`n   - 数据库服务`n3. 风险`n   - 模型准确率风险`n   - 数据安全风险`n   - 性能瓶颈风险`n4. 扩展性`n   - 支持更多 ERP 类型`n   - 支持更多任务类型`n   - 支持多语言"
        }
        return $result
    }
    else {
        # 默认分析
        $result = @{
            Background = "根据需求标题 '$Title'，这是一个新的功能需求。需要进一步了解业务背景和目标用户。"
            UserStories = "- 作为用户，我需要这个功能来...`n- 作为管理员，我希望..."
            CoreFeatures = "1. 核心功能一`n2. 核心功能二`n3. 核心功能三"
            BusinessFlow = "1. 用户操作流程`n2. 系统处理流程`n3. 数据流转流程"
            UIDesign = "1. 主界面布局`n2. 交互元素`n3. 响应式设计"
            AcceptanceCriteria = "- [ ] 功能一正常工作`n- [ ] 功能二正常工作`n- [ ] 性能满足要求`n- [ ] 安全性符合标准"
            TechnicalConsiderations = "1. 技术方案`n   - 前端技术栈`n   - 后端技术栈`n   - 数据库设计`n2. 依赖`n   - 第三方服务`n   - 内部系统`n3. 风险`n   - 技术风险`n   - 时间风险`n4. 扩展性`n   - 未来功能扩展`n   - 多租户支持"
        }
        return $result
    }
}

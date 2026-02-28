#!/usr/bin/env python3
"""
云效 CLI 配置工具 - 交互式认证和组织选择
类似 gh auth 命令，提供友好的配置体验
"""

import os
import sys
import json
import getpass
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, List, Dict, Any

# 配置常量
DEFAULT_DOMAIN = "devops.aliyun.com"
CONFIG_DIR = Path.home() / ".yunxiao"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """加载现有配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_config(config: Dict[str, Any]):
    """保存配置到文件"""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"\n✓ 配置已保存到：{CONFIG_FILE}")


def get_token_interactive() -> str:
    """交互式获取个人访问令牌"""
    print("\n📋 获取个人访问令牌")
    print("-" * 50)
    print("请访问：https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token")
    print("获取云效个人访问令牌 (Personal Access Token)\n")
    
    while True:
        token = getpass.getpass("请输入个人访问令牌 (x-yunxiao-token): ").strip()
        if token:
            # 简单验证令牌格式
            if token.startswith("pt-") or len(token) >= 20:
                return token
            else:
                print("⚠  令牌格式可能不正确，请确认")
                confirm = input("仍要继续吗？(y/N): ").strip().lower()
                if confirm == 'y':
                    return token
        else:
            print("⚠  令牌不能为空")


def get_domain_interactive() -> str:
    """交互式获取服务接入点"""
    print("\n🌐 服务接入点配置")
    print("-" * 50)
    print(f"默认域名：{DEFAULT_DOMAIN}")
    print("如果是专属版部署，请输入自定义域名\n")
    
    domain = input(f"请输入域名 [{DEFAULT_DOMAIN}]: ").strip()
    return domain if domain else DEFAULT_DOMAIN


def fetch_organizations(token: str, domain: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    通过云效 API 获取组织列表
    
    API: GET https://{domain}/oapi/v1/platform/organizations
    """
    url = f"https://{domain}/oapi/v1/platform/organizations"
    
    # 构建查询参数
    params = []
    if user_id:
        params.append(f"userId={user_id}")
    params.append("page=1")
    params.append("perPage=100")
    
    if params:
        url += "?" + "&".join(params)
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "x-yunxiao-token": token
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # 检查响应头中的分页信息
            total = response.headers.get('x-total', '0')
            total_pages = response.headers.get('x-total-pages', '1')
            
            print(f"\n📊 查询结果：共 {total} 个组织，{total_pages} 页")
            
            if isinstance(data, list):
                return data
            else:
                print(f"⚠  意外的响应格式：{type(data)}")
                return []
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ""
        print(f"\n❌ API 请求失败：HTTP {e.code}")
        print(f"错误信息：{error_body}")
        raise Exception(f"API 请求失败：{e.code}")
    except urllib.error.URLError as e:
        print(f"\n❌ 网络错误：{e.reason}")
        raise Exception(f"网络错误：{e.reason}")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        raise


def select_organization(organizations: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """让用户选择默认组织"""
    if not organizations:
        print("\n⚠  未找到任何组织")
        return None
    
    print("\n🏢 选择默认组织")
    print("-" * 50)
    
    # 显示组织列表
    for i, org in enumerate(organizations, 1):
        org_id = org.get('id', 'N/A')
        org_name = org.get('name', '未命名')
        org_desc = org.get('description', '')
        print(f"  {i}. {org_name}")
        print(f"     ID: {org_id}")
        if org_desc:
            print(f"     描述：{org_desc}")
        print()
    
    # 用户选择
    while True:
        try:
            choice = input(f"请选择组织编号 (1-{len(organizations)}): ").strip()
            if not choice:
                print("⚠  请输入有效的编号")
                continue
            
            idx = int(choice) - 1
            if 0 <= idx < len(organizations):
                selected = organizations[idx]
                print(f"\n✓ 已选择：{selected.get('name', 'N/A')} ({selected.get('id', 'N/A')})")
                return selected
            else:
                print(f"⚠  编号超出范围 (1-{len(organizations)})")
        except ValueError:
            print("⚠  请输入有效的数字")


def setup_environment(org_id: str, domain: str, token: str):
    """设置环境变量提示"""
    print("\n🔧 环境变量配置")
    print("-" * 50)
    print("请将以下环境变量添加到你的 shell 配置文件中：\n")
    
    print("# Windows PowerShell (~\\Documents\\WindowsPowerShell\\Microsoft.PowerShell_profile.ps1)")
    print(f'$env:YUNXIAO_TOKEN = "{token[:10]}...{token[-4:]}"  # 实际使用时请填入完整令牌')
    print(f'$env:YUNXIAO_DOMAIN = "{domain}"')
    print(f'$env:YUNXIAO_ORG_ID = "{org_id}"')
    print()
    print("# 或者添加到系统环境变量 (需要管理员权限)")
    print(f'[Environment]::SetEnvironmentVariable("YUNXIAO_TOKEN", "...", "User")')
    print(f'[Environment]::SetEnvironmentVariable("YUNXIAO_DOMAIN", "{domain}", "User")')
    print(f'[Environment]::SetEnvironmentVariable("YUNXIAO_ORG_ID", "{org_id}", "User")')
    print()
    
    # 也可以直接写入 .env 文件
    env_file = Path.cwd() / ".env.yunxiao"
    print(f"或者创建 .env 文件：{env_file}")
    
    return {
        "YUNXIAO_TOKEN": token,
        "YUNXIAO_DOMAIN": domain,
        "YUNXIAO_ORG_ID": org_id
    }


def main():
    """主函数"""
    print("=" * 60)
    print("  云效 CLI 配置工具")
    print("  Yunxiao Interactive Configuration")
    print("=" * 60)
    
    try:
        # 步骤 1: 获取个人访问令牌
        token = get_token_interactive()
        
        # 步骤 2: 获取服务接入点
        domain = get_domain_interactive()
        
        # 步骤 3: 获取组织列表
        print("\n🔄 正在获取组织列表...")
        organizations = fetch_organizations(token, domain)
        
        if not organizations:
            print("\n⚠  未获取到组织列表，请检查令牌和域名配置")
            return 1
        
        # 步骤 4: 选择默认组织
        selected_org = select_organization(organizations)
        if not selected_org:
            print("\n⚠  未选择组织，配置中止")
            return 1
        
        org_id = selected_org.get('id')
        
        # 步骤 5: 保存配置
        config = {
            "token": token,
            "domain": domain,
            "organization_id": org_id,
            "organization_name": selected_org.get('name'),
            "updated_at": Path(CONFIG_FILE).stat().st_mtime if Path(CONFIG_FILE).exists() else None
        }
        save_config(config)
        
        # 步骤 6: 环境变量提示
        setup_environment(org_id, domain, token)
        
        print("\n" + "=" * 60)
        print("  ✅ 配置完成!")
        print("=" * 60)
        print(f"\n当前配置:")
        print(f"  • 域名：{domain}")
        print(f"  • 组织：{selected_org.get('name')} ({org_id})")
        print(f"  • 配置文件：{CONFIG_FILE}")
        print("\n下一步:")
        print("  1. 将环境变量添加到你的 shell 配置文件")
        print("  2. 重启终端或运行：refreshenv (Windows)")
        print("  3. 开始使用云效 CLI 命令\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠  配置已取消")
        return 130
    except Exception as e:
        print(f"\n❌ 配置失败：{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

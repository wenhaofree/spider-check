import requests
import json
from datetime import datetime

def checkin(cookie):
    """
    执行 ikuuu 网站的签到操作
    
    Args:
        cookie (str): 用户的 cookie 字符串
    
    Returns:
        dict: 签到结果
    """
    url = "https://ikuuu.one/user/checkin"
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        response = requests.post(url, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"ret": 0, "msg": f"请求失败: {str(e)}"}
    except json.JSONDecodeError:
        return {"ret": 0, "msg": "解析响应失败"}

def get_email_from_cookie(cookie):
    """从 cookie 中提取邮箱信息"""
    try:
        for item in cookie.split(';'):
            if 'email=' in item:
                return item.split('=')[1].replace('%40', '@').strip()
    except:
        return "未知用户"
    return "未知用户"

def main():
    # 多个用户的 cookie 列表
    cookies = [
        "_ga_8HVN7928SC=GS1.1.1738654631.5.1.1738654732.0.0.0; _ga=GA1.2.96918656.1736923678; _gid=GA1.2.2059163996.1738654631; _gat_gtag_UA_158605448_1=1; email=767137738%40qq.com; expire_in=1739259430; ip=23d90fbcb61251e5b4119003ef73c77b; key=7c25f5b0d20da8ddb3c1e3bb304f5c1bc7369de56a200; uid=3150318; lang=zh-cn",
        "lang=en; uid=2570254; email=fuwenhao945%40gmail.com; key=05b22c6deadc449f70bf124cc6593169a9597b097f8e8; ip=cc283181d98e65a829ea378b862ef1d1; expire_in=1739109859; _gid=GA1.2.1885324804.1738654876; _gat_gtag_UA_158605448_1=1; _ga_8HVN7928SC=GS1.1.1738654875.50.1.1738654882.0.0.0; _ga=GA1.1.1898060659.1731203562"
        # 在这里添加更多用户的 cookie
    ]
    
    print(f"\n=== ikuuu 签到任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    for cookie in cookies:
        email = get_email_from_cookie(cookie)
        result = checkin(cookie)
        
        if result.get('ret') == 1:
            print(f"用户 {email} 签到成功：{result.get('msg')}")
        else:
            print(f"用户 {email} 签到失败：{result.get('msg', '未知错误')}")
        print("-" * 50)
    
    print(f"\n=== 签到任务结束 - 共处理 {len(cookies)} 个账号 ===\n")

if __name__ == "__main__":
    main()

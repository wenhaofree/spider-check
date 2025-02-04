import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """配置日志"""
    # 创建 logs 目录（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 配置日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 创建日志处理器
    file_handler = RotatingFileHandler(
        'logs/ikuu.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    console_handler = logging.StreamHandler()
    
    # 设置日志格式
    formatter = logging.Formatter(log_format, date_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

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

def load_cookies_from_env():
    """从环境变量加载所有 cookie"""
    cookies = []
    i = 1
    while True:
        cookie = os.getenv(f'COOKIE_{i}')
        if not cookie:
            break
        cookies.append(cookie)
        i += 1
    return cookies

def main():
    # 设置日志
    logger = setup_logger()
    
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取 cookies
    cookies = load_cookies_from_env()
    
    if not cookies:
        logger.error("未找到任何 cookie 配置，请检查 .env 文件")
        return
    
    logger.info(f"=== ikuuu 签到任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    success_count = 0
    fail_count = 0
    
    for cookie in cookies:
        email = get_email_from_cookie(cookie)
        result = checkin(cookie)
        
        if result.get('ret') == 1:
            success_count += 1
            logger.info(f"用户 {email} 签到成功：{result.get('msg')}")
        else:
            fail_count += 1
            logger.error(f"用户 {email} 签到失败：{result.get('msg', '未知错误')}")
        logger.info("-" * 50)
    
    logger.info(f"=== 签到任务结束 - 共处理 {len(cookies)} 个账号 ===")
    logger.info(f"成功：{success_count} 个，失败：{fail_count} 个")

if __name__ == "__main__":
    main()

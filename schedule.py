import time
from datetime import datetime
import subprocess
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """配置日志"""
    if not hasattr(setup_logger, 'logger'):
        # 创建 logs 目录（如果不存在）
        import os
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # 配置日志格式
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # 创建日志处理器
        file_handler = RotatingFileHandler(
            'logs/schedule.log',
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
        
        setup_logger.logger = logger
    
    return setup_logger.logger

def run_ikuu():
    """运行 ikuu.py 脚本"""
    try:
        subprocess.run(['python', 'ikuu.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger = setup_logger()
        logger.error(f"运行 ikuu.py 失败: {str(e)}")
        return False

def wait_until_next_run(hour=8, minute=0):
    """等待到下一次运行时间"""
    now = datetime.now()
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    if next_run <= now:
        next_run = next_run.replace(day=next_run.day + 1)
    
    wait_seconds = (next_run - now).total_seconds()
    return wait_seconds

def main():
    logger = setup_logger()
    logger.info("定时任务启动")
    
    # 首次运行
    logger.info("执行首次签到")
    run_ikuu()
    
    while True:
        try:
            # 等待到下一次运行时间（每天早上 8:00）
            wait_time = wait_until_next_run(hour=8, minute=0)
            logger.info(f"等待下次运行，将在 {wait_time/3600:.2f} 小时后执行")
            time.sleep(wait_time)
            
            # 执行签到
            logger.info("开始执行定时签到")
            run_ikuu()
            
        except KeyboardInterrupt:
            logger.info("程序被用户中断")
            break
        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
            # 等待 5 分钟后重试
            time.sleep(300)

if __name__ == "__main__":
    main()

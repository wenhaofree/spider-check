import time
import schedule
import logging
from logging.handlers import RotatingFileHandler
from ikuu import main

def setup_logger():
    """配置日志"""
    # 创建 logs 目录（如果不存在）
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 配置日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 创建日志处理器
    file_handler = RotatingFileHandler(
        'logs/ikuu_schedule.log',
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

def job():
    logger = logging.getLogger()
    main()
    logger.info('IKUU采集程序结束时间: %s', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

def schedule_job():
    logger = logging.getLogger()
    # schedule.every(3).hours.do(job)  # 一天六次
    # schedule.every(1).days.do(job)
    schedule.every().day.at("00:00").do(job)  # 每天凌晨执行
    logger.info('定时任务已设置：每天 00:00 执行')

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    logger = setup_logger()
    logger.info('程序启动...IKUU数据采集')
    schedule_job()

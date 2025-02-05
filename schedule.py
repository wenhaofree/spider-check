import time

import schedule

from ikuu import main


def job():
    main()
    print('[知识星球采集程序结束时间: %s]' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def schedule_job():
    # schedule.every(3).hours.do(job)  # 一天六次
    schedule.every(1).days.do(job)
    # schedule.every().day.at("00:00").do(job)  # 每天凌晨执行

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    print('[程序启动...知识星球数据采集]')
    schedule_job()

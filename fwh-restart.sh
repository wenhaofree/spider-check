#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到脚本所在目录
cd "$SCRIPT_DIR"

# 查找并终止现有的 Python 进程
PID=$(pgrep -f "python3 schedule.py")
if [ ! -z "$PID" ]; then
    echo "正在终止现有进程..."
    echo "进程 ID: $PID"
    kill $PID
    sleep 2
    echo "✓ 原进程已成功终止"
fi

# 启动 Python 脚本并在后台运行
echo "正在启动定时任务程序..."
nohup python3 schedule.py > logs/schedule.log 2>&1 &
NEW_PID=$!

# 检查进程是否成功启动
if ps -p $NEW_PID > /dev/null; then
    echo "✓ 定时任务程序启动成功"
    echo "新进程 ID: $NEW_PID"
    echo "日志文件位置: $SCRIPT_DIR/logs/schedule.log"
else
    echo "✗ 程序启动失败，请检查日志文件"
    exit 1
fi
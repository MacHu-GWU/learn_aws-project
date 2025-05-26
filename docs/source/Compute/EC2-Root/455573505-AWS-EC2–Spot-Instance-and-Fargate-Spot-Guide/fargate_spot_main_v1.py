# -*- coding: utf-8 -*-

import os
import time
import signal

terminate = False


def handle_signal(signum, frame):
    global terminate
    print(f"接收到信号: {signum}，准备终止程序。")
    terminate = True


# 注册信号处理函数
signal.signal(signal.SIGTERM, handle_signal)  # 处理容器终止
signal.signal(signal.SIGINT, handle_signal)  # 处理 Ctrl+C 中断


def main():
    print(f"主程序 PID: {os.getpid()}")
    print("程序开始运行。按 Ctrl+C 或发送 SIGTERM 信号以终止。")
    n_job = 10  # 模拟的任务数量
    for ith in range(1, 1 + n_job):
        print(f"正在处理第 {ith} 个任务...")
        time.sleep(5)
        print("任务处理完成。")
        if terminate:
            print("执行清理操作...")
            print("程序已优雅地终止。")
            print(f"已完成 {ith} 个任务。")
            return ith

    print("所有任务已完成。")
    return n_job


if __name__ == "__main__":
    main()

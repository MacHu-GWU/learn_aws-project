# -*- coding: utf-8 -*-

import os
import time
import signal
import dataclasses


class TerminateException(Exception):
    """自定义异常，用于处理终止信号时的特殊情况。"""

    pass


def handle_signal(signum, frame):
    print(f"接收到信号: {signum}，准备终止程序。")
    raise TerminateException


# 注册信号处理函数
signal.signal(signal.SIGTERM, handle_signal)  # 处理容器终止
signal.signal(signal.SIGINT, handle_signal)  # 处理 Ctrl+C 中断


@dataclasses.dataclass
class Task:
    id: int

    def process(self):
        print(f"处理任务 {self.id = }...")
        time.sleep(5)

    def save_checkpoint(self):
        print(f"保存检查点 {self.id = } ...")


def main(tasks: list[Task]):
    print(f"主程序 PID: {os.getpid()}")
    print("程序开始运行。按 Ctrl+C 或发送 SIGTERM 信号以终止。")
    for ith, task in enumerate(tasks, start=1):
        try:
            task.process()
            task.save_checkpoint()
        except TerminateException:
            print(f"任务 {task.id} 处理被终止。")
            print("执行清理操作...")
            print("程序已优雅地终止。")
            print(f"已完成 {ith} 个任务。")
            return ith
    print("所有任务已完成。")
    return ith


if __name__ == "__main__":
    n_task = 10  # 模拟的任务数量
    tasks = [Task(id=i) for i in range(1, 1 + n_task)]
    main(tasks)

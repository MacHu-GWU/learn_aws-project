# -*- coding: utf-8 -*-

import os
import signal

# 替换为 main.py 的 pid
target_pid = 12345  # 请将此处的 12345 替换为实际的 PID

# 等待一段时间后发送信号
print(f"向 PID {target_pid} 发送 SIGTERM 信号。")
os.kill(target_pid, signal.SIGTERM)
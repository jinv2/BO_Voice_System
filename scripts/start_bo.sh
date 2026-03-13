#!/bin/bash
# Shensist 守护进程启动脚本
echo "正在激活‘驳’(BO) 后台位面..."
nohup python3 src/bo_cli.py --mode voice > /dev/null 2>&1 &
echo "‘驳’已进入后台，随时听候指令。"
notify-send "神思矩阵" "‘驳’智能体已进入后台常驻状态。"

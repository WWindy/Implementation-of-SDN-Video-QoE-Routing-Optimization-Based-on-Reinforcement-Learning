# -*-coding:UTF-8 -*-
import subprocess
import time
# 开启Wireshark抓包
subprocess.Popen(["sudo", "tshark", "-i", "eth0", "-w", "capture.pcap"])

# 根据需要调整抓包时间
time.sleep(10)

# 关闭Wireshark抓包
p = subprocess.Popen(["sudo", "killall", "tshark"])

# 使用tshark命令分析抓取的数据包，并计算视频码率
with open("capture.pcap", "rb") as f:
    p2 = subprocess.Popen(["tshark", "-r", "-", "-qz", "io,stat,0.1", "-z", "conv,udp", "-z", "io,stat,0.1", "-z", "io,stat,0.1", "-z", "io,stat,0.1"],
                          stdin=f, stdout=subprocess.PIPE)
    for line in iter(p2.stdout.readline, ""):
        print(line)


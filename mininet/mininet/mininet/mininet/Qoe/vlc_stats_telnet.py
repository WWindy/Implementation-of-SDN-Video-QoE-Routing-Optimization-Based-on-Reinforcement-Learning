# -*-coding:UTF-8 -*-
import telnetlib
import time

# 创建一个Telnet对象并连接到VLC命令行界面
tn = telnetlib.Telnet('localhost', 1234)
tn.write(b'login\n')
tn.read_until(b'Password: ')
tn.write(b'admin\n')
tn.read_until(b'>')
tn.write(b'info\n')

# 打开文件并开始记录播放统计信息
with open('vlc_stats.txt', 'w') as f:
    while True:
        # 获取并解码命令行输出
        output = tn.read_until(b'>').decode('utf-8')
        # 提取视频统计信息
        stats = [line.strip() for line in output.split('\n') if line.startswith('Stream')]
        # 将统计信息写入文件
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        f.write('\n'.join(stats) + '\n\n')
        f.flush()

# -*-coding:UTF-8 -*-
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController,Controller
from datetime import datetime
import pyshark
import subprocess
import os
from scapy.all import *
net=Mininet(controller=RemoteController)
odl_controller=net.addController('ODL_controller',controller= RemoteController,ip='192.168.238.132',port=6653)#ip地址为实际环境中控制器的IP地址

s1=net.addSwitch('s1')
s2=net.addSwitch('s2')
s3=net.addSwitch('s3')
s4=net.addSwitch('s4')

h1=net.addHost('h1')
h2=net.addHost('h2')

net.addLink(s1,h1)
net.addLink(s2,h2)

net.addLink(s1,s3)
net.addLink(s2,s3)

net.addLink(s1,s4)
net.addLink(s2,s4)


h1.setIP('10.0.0.1',24)
h2.setIP('10.0.0.2',24)

net.start()

os.system('ovs-ofctl del-flows s1')
os.system('ovs-ofctl del-flows s2')
os.system('ovs-ofctl del-flows s3')
os.system('ovs-ofctl del-flows s4')

net.pingAll()
net.pingAll()
net.pingAll()

# 在 Python 文件中运行 tcpdump 并保存输出到文件
h2.cmd('tcpdump -i h2-eth0 udp port 1234 -w capture.pcap &')

# 运行视频播放命令
h1.cmd('xterm -hold -e "vlc-wrapper -vvv /home/windy/Redios/chat.avi --loop --sout udp:10.0.0.2:1234 --ttl 10" &')
h2.cmd('xterm -hold -e "vlc-wrapper udp://@:1234" &')

print("display")

# 等待一段时间以便视频数据能够传输
time.sleep(10)

h2.cmd('timeout 35 xterm -hold -e "iperf -u -s" &')
h1.cmd('timeout 35 xterm -hold -e "iperf -u -c 10.0.0.2 -b 300M -t 30" &')
# 打开捕获的数据包文件
cap = pyshark.FileCapture('/home/windy/mininet/custom/Qoe/5.23/capture.pcap', keep_packets=True, display_filter='udp.port == 1234')


print(cap)

# 查找视频数据流的流量和持续时间
video_stream = cap[0]
print(cap[0])
print(type(video_stream.sniff_time))

timestamp=time.mktime(video_stream.sniff_time.timetuple())
print("timestamp")
print(timestamp)
start_time = float(timestamp)
end_time = float(timestamp)
total_bytes = int(timestamp)
frame_count=0
for packet in cap:
	if 'udp' in packet and packet['udp'].dstport == '1234':
		end_time = float(time.mktime(packet.sniff_time.timetuple()))
		total_bytes += int(packet.length)
		frame_count+=1
	else:
		print(frame_count)
# 计算视频流的平均帧率和码率
duration = end_time - start_time
frame_rate = None
bit_rate = None
print("frame_count")
print(frame_count)
print("start get")

if duration > 0:
	#frame_count = int(cap[1].video.frame_count)
	frame_rate = frame_count / duration
	bit_rate = (total_bytes * 8) / duration / 1000000  # Mbps

print('Duration: {} seconds'.format(duration))
print('Frame rate: {} fps'.format(frame_rate))
print('Bit rate: {} Mbps'.format(bit_rate))

# 停止 tcpdump 并将数据包保存到本地
#h2.cmd('kill %tcpdump')
#os.remove("capture.pcap")
#h2.cmd('gzip capture.pcap')
#hs2.cmd('mv capture.pcap.gz /tmp/')

# 命令行界面
CLI(net)

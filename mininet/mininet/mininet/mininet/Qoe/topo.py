# -*-coding:UTF-8 -*-
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController ,Controller


import subprocess
import os

net=Mininet(controller=RemoteController)
odl_controller=net.addController('ODL_controller',controller= RemoteController,ip='192.168.238.132',port=6653)#ip地址为实际环境中控制器的IP地址

from scapy.all import *
# and (udp contains \"AVC\" or udp contains \"H264\")
# 过滤器，用于过滤UDP视频流数据包
# udp_filter = "udp port 1234"
# 全局变量，用于保存捕获到的数据包和计数
packets = []
count = 0


def my_telnet():
	# 在命令行中执行sudo命令
	cmd = "sudo apt-get update"
	p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	# 输入sudo命令需要的密码
	password = "123456\n"
	p.stdin.write(password.encode())

	# 读取sudo命令的输出
	output, err = p.communicate()

	# 输出结果
	print(output.decode())


# 回调函数，用于处理捕获的数据包
# packet捕获的数据包
def process_packet(packet):
	global count, packets
	print("---------get-----------")
	if packet.haslayer(UDP):
		if packet[UDP].dport == 1234:
			if packet.haslayer(Raw):
				if "AVC" in packet[Raw].load or "H264" in packet[Raw].load:
					# 处理捕获到的视频流数据包
					if count < 50:
						packets.append(packet)
						count += 1
					else:
						packets.pop(0)
						packets.append(packet)
					print("-----------------save-------------")
					# 保存最新的50个数据包到文件
					wrpcap("/home/windy/mininet/custom/wout.pcap", packets)


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
my_telnet()

h1.cmd('xterm -hold -e "vlc-wrapper -vvv /home/windy/Redios/chat.avi --loop --sout udp:10.0.0.2:1234 --ttl 10" &')
h2.cmd('xterm -hold -e "vlc-wrapper udp://@:1234" &')

# h1.cmd('xterm -hold -e "vlc-wrapper -vvv /home/windy/Redios/chat.m4v --sout-ffmpeg-strict=-2 --no-sout-audio --sout "#rtp{dst=10.0.0.2,port=1234,ttl=1}"" &')
# h1.cmd('xterm -hold -e "vlc-wrapper -vvv /home/windy/Redios/chat.m4v --sout udp:10.0.0.2:1234 --ttl 10" &')
# h2.cmd('xterm -hold -e "vlc-wrapper udp://@:1234 --vout=dummy --no-audio --no-sub-autodetect-file --no-osd --no-stats --no-repeat --loop" &')

#h2.cmd('python vlc_stats_telnet.py > vlc_stats.txt 2>&1 &')
# print("-----------start------------")
# sniff(filter="udp", prn=process_packet)
h2.cmd('sudo python h2.py > h2_result.txt 2>&1 &')
CLI(net)




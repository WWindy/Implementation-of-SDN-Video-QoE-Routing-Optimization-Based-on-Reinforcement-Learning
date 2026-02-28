# -*-coding:UTF-8 -*-
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController ,Controller
import os
import random
from datetime import datetime
import pyshark
import subprocess
from timeout_decorator import timeout
from scapy.all import *
import sys
sys.path.append('/home/windy/mininet_web')
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mininet_web.settings")# project_name 项目名称
django.setup()

from myproject.models import flows,Switch,Host,Info,Info_op

class Net():
	end_time_temp=0
	total_bytes_temp=0
	frame_count_temp=0
	frame_rate=0
	bit_rate=0
	rm=0
	def init(self):
		self.total_bytes=0
		self.frame_count=0
		self.end_time=0

		self.hostnum=5
		self.net=Mininet(controller=RemoteController)
		self.odl_controller=self.net.addController('ODL_controller',controller= RemoteController,autoSetMacs=False, build=False,ip='192.168.238.132',port=6653)#ip地址为实际环境中控制器的IP地址
		s1=self.net.addSwitch('s1')
		s2=self.net.addSwitch('s2')
		s3=self.net.addSwitch('s3')
		s4=self.net.addSwitch('s4')
		s5=self.net.addSwitch('s5')

		h1=self.net.addHost('h1')
		h2=self.net.addHost('h2')
		h3=self.net.addHost('h3')
		h4=self.net.addHost('h4')
		h5=self.net.addHost('h5')


		self.net.addLink(s1,h1)
		self.net.addLink(s2,h2)
		self.net.addLink(s3,h3)
		self.net.addLink(s4,h4)
		self.net.addLink(s5,h5)

		self.net.addLink(s1,s2)
		self.net.addLink(s1,s4)
		self.net.addLink(s1,s5)
		self.net.addLink(s1,s3)

		self.net.addLink(s2,s4)
		self.net.addLink(s2,s5)
		self.net.addLink(s2,s3)

		#self.net.addLink(s3,s4)
		#self.net.addLink(s3,s5)


		#self.net.addLink(s4,s5)


		h1.setIP('10.0.0.1',24)
		h2.setIP('10.0.0.2',24)
		h3.setIP('10.0.0.3',24)
		h4.setIP('10.0.0.4',24)
		h5.setIP('10.0.0.5',24)



		self.net.start()

		os.system('ovs-ofctl del-flows s1')
		os.system('ovs-ofctl del-flows s2')
		os.system('ovs-ofctl del-flows s3')
		os.system('ovs-ofctl del-flows s4')
		os.system('ovs-ofctl del-flows s5')
		#self.net.iperfUdp("bw h1 h2")
		#self.iperf()
		self.net.pingAll()
		self.net.pingAll()
	
	def check_process_running(self,process_name):
		ps = subprocess.Popen('ps aux | grep ' + process_name, shell=True, stdout=subprocess.PIPE)
		output = ps.stdout.read()
		ps.stdout.close()
		ps.wait()
		 # 如果输出中包含给定的进程，则该进程正在运行
		return process_name in output	


	def get_fr_br(self):
		
		h2 = self.net.get('h2')
		if Net.rm==10:
			Net.rm=0

		else:Net.rm+=1
		time.sleep(1)
		a=str(int(time.time()))
		h2.cmd('tcpdump -i h2-eth0 -c 100 udp port 1234 -w /home/windy/mininet/custom/pcap/capture'+a+'.pcap &')
		time.sleep(10)
		cap = pyshark.FileCapture('/home/windy/mininet/custom/pcap/capture'+a+'.pcap', keep_packets=True, display_filter='udp.port == 1234')
		timestamp=time.mktime(cap[0].sniff_time.timetuple())
		start_time = float(timestamp)
		self.end_time = float(timestamp)
		self.total_bytes = 0
		self.frame_count=0
		if cap : print("cap is null")
		try:

		    def read_packets():
			    for packet in cap:
				if 'udp' in packet and packet['udp'].dstport == '1234':
				    self.end_time = float(time.mktime(packet.sniff_time.timetuple()))
				    self.total_bytes += int(packet.length)
				    self.frame_count+=1
				    Net.end_time_temp=self.end_time
				    Net.total_bytes_temp=self.total_bytes
				    Net.frame_count_temp=self.frame_count
		    read_packets()
		except Exception as e:#运行出错，取最近一次的数据来“糊弄”，防止程序终端运行
		    print('have some Error while reading packets from capture file ,we use last data')
		    self.end_time=Net.end_time_temp
		    self.total_bytes=Net.total_bytes_temp
		    self.frame_count=Net.frame_count_temp
		finally:
		    if cap:cap.close()
		# 计算视频流的平均帧率和码率
		duration = self.end_time - start_time
		if duration > 0:
			Net.frame_rate = self.frame_count / duration
			Net.bit_rate = (self.total_bytes * 8) / duration / 1000000  # Mbps

		
		return Net.frame_rate,Net.bit_rate
	
	def iperf(self):
		self.net.pingAll()
		self.net.pingAll()
		self.net.iperfMulti("25M",10,1,2)
		#os.systerm('iperfmulti 25M 10 1 2')
		#CLI(net)
	def daikuan(self,src,dst):
		command="bw "+src+" "+dst
		return self.net.iperfUdp(command)
	def stream(self):
		# get host
		h1 = self.net.get('h1')
		h2 = self.net.get('h2')
		# xterm
		h1.cmd('xterm -hold -e "vlc-wrapper -vvv /home/windy/Redios/chat.avi --loop --sout udp:10.0.0.2:1234 --ttl 10" &')
		h2.cmd('xterm -hold -e "vlc-wrapper udp://@:1234" &')
	def stream1(self):
		# get host
		start=0
		end=0
		while start==end:
			start=random.randint(3,5)
			end=random.randint(3,5)
		
		if random.randint(1,1)==1:
			print("now start flows between %d"%(start)+" and %d "%(end)+"!!!!!!!!!!!!!!!!!!!!!")
			hstart = self.net.get('h'+str(start))
			hend = self.net.get('h'+str(end))
			# xterm
			hstart.cmd('timeout 240 xterm -hold -e "vlc-wrapper -vvv /home/windy/Redios/chat.avi --loop --sout udp:10.0.0.'+str(end)+':2345 --ttl 10" &')
			hend.cmd('xterm -hold -e "vlc-wrapper udp://@:2345" &')

	def sed_ganrao(self):
		start=0
		end=0
		if random.randint(1,2)==1:
			start1=0
			while start==end or start1==end:
				start=random.randint(1,5)
				end=random.randint(1,5)
				start1=random.randint(1,5)
			
			bandwidth=random.randint(100,500)
			print("now start flows between h%d"%(start)+" and h%d "%(end)+"!!!!!!!!!!!!!!!!!!!!!")
			hstart = self.net.get('h'+str(start))
			hend = self.net.get('h'+str(end))
			hend.cmd('timeout 35 xterm -hold -e "iperf -u -s" &')
			hstart.cmd('timeout 35 xterm -hold -e "iperf -u -c 10.0.0.'+str(end)+' -b '+str(bandwidth)+'M -t 30" &')

			if start1!=start:
				bandwidth=random.randint(100,700)
				print("now start flows between h%d"%(start1)+" and h%d "%(end)+"!!!!!!!!!!!!!!!!!!!!!")
				hstart1=self.net.get('h'+str(start1))
				hstart1.cmd('timeout 35 xterm -hold -e "iperf -u -c 10.0.0.'+str(end)+' -b '+str(bandwidth)+'M -t 30" &')
				

	def databases_host(self):
		Host.objects.all().delete()
		for i in range(1,self.hostnum+1):
			h = self.net.get('h'+str(i))
			host=Host(id_num=i,ip='10.0.0.'+str(i),mac=h.MAC())
			host.save()
	def printt(self):#输出网络中物理链路
		for link in self.net.links:
    			print(link)



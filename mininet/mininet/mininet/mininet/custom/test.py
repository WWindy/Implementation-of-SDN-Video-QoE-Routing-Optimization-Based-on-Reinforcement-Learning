#coding=UTF-8
#!/usr/bin/env python
from __future__ import division
import requests
from sklearn.preprocessing import normalize
from requests.auth import HTTPBasicAuth
import json
import unicodedata
from subprocess import Popen, PIPE
import time
import networkx as nx
from sys import exit
import re
#import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import matplotlib.pyplot as plt
import gym
import os
import subprocess
import time
from testtopo import Net
import threading
import numpy as np
import sys
sys.path.append('/home/windy/mininet_web')
import os,django
from myproject.models import flows,Switch,Host,Info,Info_op,result
from django.db.models import Q
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mininet_web.settings")# project_name 项目名称
django.setup()



global Randomly_decide_to_send_interfering_streams,switch_number,controller_ip
Randomly_decide_to_send_interfering_streams=True
controller_ip="192.168.238.132"
switch_number=input("请输入当前网络交换机个数")
Net=Net()
Net.init()#初始化网络拓扑
EP_MAX = 1000
EP_LEN = 33
GAMMA = 0.9
A_LR = 0.0001
C_LR = 0.0002
BATCH = 32
A_UPDATE_STEPS = 10
C_UPDATE_STEPS = 10
S_DIM, A_DIM = switch_number*switch_number,4
METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][0]        # choose the method for optimization

class PPO(object):

    def __init__(self):
        self.sess = tf.Session()
        self.tfs = tf.placeholder(tf.float32, [None, S_DIM], 'state')

        # critic
        with tf.variable_scope('critic'):
            l1 = tf.layers.dense(self.tfs, 100, tf.nn.relu)
            self.v = tf.layers.dense(l1, 1,activation=None)
            self.tfdc_r = tf.placeholder(tf.float32, [None, 1], 'discounted_r')
            self.advantage = self.tfdc_r - self.v
            self.closs = tf.reduce_mean(tf.square(self.advantage))
            self.ctrain_op = tf.train.AdamOptimizer(C_LR).minimize(self.closs)

        # actor
        pi, pi_params = self._build_anet('pi', trainable=True)
        oldpi, oldpi_params = self._build_anet('oldpi', trainable=False)
        with tf.variable_scope('sample_action'):
            self.sample_op = tf.squeeze(pi.sample(1), axis=0)       # choosing action
            #self.sample_op =pi.sample(1)
            
        with tf.variable_scope('update_oldpi'):
            self.update_oldpi_op = [oldp.assign(p) for p, oldp in zip(pi_params, oldpi_params)]

        self.tfa = tf.placeholder(tf.float32, [None, A_DIM], 'action')
        self.tfadv = tf.placeholder(tf.float32, [None, 1], 'advantage')
        with tf.variable_scope('loss'):
            with tf.variable_scope('surrogate'):
                # ratio = tf.exp(pi.log_prob(self.tfa) - oldpi.log_prob(self.tfa))
                ratio = pi.prob(self.tfa) / (oldpi.prob(self.tfa) + 1e-5)
                surr = ratio * self.tfadv
            if METHOD['name'] == 'kl_pen':
                self.tflam = tf.placeholder(tf.float32, None, 'lambda')
                kl = tf.distributions.kl_divergence(oldpi, pi)
                self.kl_mean = tf.reduce_mean(kl)
                self.aloss = -(tf.reduce_mean(surr - self.tflam * kl))
            else:   # clipping method, find this is better
                self.aloss = -tf.reduce_mean(tf.minimum(
                    surr,
                    tf.clip_by_value(ratio, 1.-METHOD['epsilon'], 1.+METHOD['epsilon'])*self.tfadv))

        with tf.variable_scope('atrain'):
            self.atrain_op = tf.train.AdamOptimizer(A_LR).minimize(self.aloss)

        tf.summary.FileWriter("log/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())

    def update(self, s, a, r):
        self.sess.run(self.update_oldpi_op)
        adv = self.sess.run(self.advantage, {self.tfs: s, self.tfdc_r: r})


        # update actor
        if METHOD['name'] == 'kl_pen':
            for _ in range(A_UPDATE_STEPS):
                _, kl = self.sess.run(
                    [self.atrain_op, self.kl_mean],
                    {self.tfs: s, self.tfa: a, self.tfadv: adv, self.tflam: METHOD['lam']})
                if kl > 4*METHOD['kl_target']:  # this in in google's paper
                    break
            if kl < METHOD['kl_target'] / 1.5:  # adaptive lambda, this is in OpenAI's paper
                METHOD['lam'] /= 2
            elif kl > METHOD['kl_target'] * 1.5:
                METHOD['lam'] *= 2
            METHOD['lam'] = np.clip(METHOD['lam'], 1e-4, 10)    # sometimes explode, this clipping is my solution
        else:   # clipping method, find this is better (OpenAI's paper)
            [self.sess.run(self.atrain_op, {self.tfs: s, self.tfa: a, self.tfadv: adv}) for _ in range(A_UPDATE_STEPS)]

        # update critic
        [self.sess.run(self.ctrain_op, {self.tfs: s, self.tfdc_r: r}) for _ in range(C_UPDATE_STEPS)]

    def _build_anet(self, name, trainable):
        with tf.variable_scope(name):
            l1 = tf.layers.dense(self.tfs, 100, tf.nn.relu, trainable=trainable)
            mu = 2 * tf.layers.dense(l1, A_DIM, tf.nn.tanh, trainable=trainable)
            sigma = tf.layers.dense(l1, A_DIM, tf.nn.softplus, trainable=trainable)
            norm_dist = tf.distributions.Normal(loc=mu, scale=sigma)
        params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope=name)
        return norm_dist, params

    def choose_action(self, s):
        s = s[np.newaxis, :]
        a = self.sess.run(self.sample_op, {self.tfs: s})[0]
        return a

    def get_v(self, s):
        if s.ndim < 2: s = s[np.newaxis, :]
        return self.sess.run(self.v, {self.tfs: s})[0, 0]

        
        
        
        



class env():

	

	# Method To Get REST Data In JSON Format
	def getResponse(self,url,choice):
		
		response = requests.get(url, auth=HTTPBasicAuth('admin', 'admin'))

		if(response.ok):
			jData = json.loads(response.content)
			if(choice=="topology"):
				self.topologyInformation(jData)
			elif(choice=="statistics"):
				return self.getStats(jData)
				
				
		else:
			response.raise_for_status()

	def topologyInformation(self,data):
		global switch
		global deviceMAC
		global deviceIP
		global hostPorts
		global linkPorts
		global G
		global cost

		for i in data["network-topology"]["topology"]:
				if i["topology-id"]!="flow:1":
					continue
				for j in i["node"]:
					# Device MAC and IP
					if i["topology-id"]!="flow:1":
						continue
					if "host-tracker-service:addresses" in j:
						for k in j["host-tracker-service:addresses"]:
							ip = k["ip"]
							mac = k["mac"]
							deviceMAC[ip] = mac
							deviceIP[mac] = ip

					# Device Switch Connection and Port

					if "host-tracker-service:attachment-points" in j:

						for k in j["host-tracker-service:attachment-points"]:
							mac = k["corresponding-tp"]
							mac = mac.split(":",1)[1]
							ip = deviceIP[mac]
							temp = k["tp-id"]
							switchID = temp.split(":")
							port = switchID[2]
							hostPorts[ip] = port
							switchID = switchID[0] + ":" + switchID[1]
							switch[ip] = switchID

		# Link Port Mapping
		for i in data["network-topology"]["topology"]:
			if i["topology-id"]!="flow:1":
					continue
			for j in i["link"]:
					if "host" not in j['link-id']:
						src = j["link-id"].split(":")
						srcPort = src[2]
						dst = j["destination"]["dest-tp"].split(":")
						dstPort = dst[2]
						srcToDst = src[1] + "::" + dst[1]
						linkPorts[srcToDst] = srcPort + "::" + dstPort
						G.add_edge((int)(src[1]),(int)(dst[1]))

	def getStats(self,data):
		global cost
		txRate = 0
		for i in data["node-connector"]:
			tx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["bytes"]["transmitted"])
		
		return tx


	def systemCommand(self,cmd):
		terminalProcess = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
		terminalOutput, stderr = terminalProcess.communicate()
	

	def pushFlowRules(self):
		global way
		global h1,h2
		global target#target=h1[-1]+":"+h2[-1]
		
		
		for currentNode in range(0, len(way[target])-1):
			if (currentNode==0):
				inport = hostPorts[h1]
				srcNode = way[target][currentNode]
				dstNode = way[target][currentNode+1]
				outport = linkPorts[srcNode + "::" + dstNode]
				outport = outport[0]
			else:
				prevNode = way[target][currentNode-1]
				srcNode = way[target][currentNode]
				dstNode = way[target][currentNode+1]
				inport = linkPorts[prevNode + "::" + srcNode]
				inport = inport.split("::")[1]
				outport = linkPorts[srcNode + "::" + dstNode]
				outport = outport.split("::")[0]

			xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>32767</priority><flow-name>Load Balance 1</flow-name><match><in-port>' + str(inport) +'</in-port><ipv4-destination>10.0.0.1/32</ipv4-destination><ipv4-source>10.0.0.2/32</ipv4-source><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>1</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(outport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>\''

			xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>32767</priority><flow-name>Load Balance 2</flow-name><match><in-port>' + str(outport) +'</in-port><ipv4-destination>10.0.0.2/32</ipv4-destination><ipv4-source>10.0.0.1/32</ipv4-source><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>2</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(inport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>\''

			flowURL = "http://"+controller_ip+":8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ way[target][currentNode] +"/table/0/flow/1"

			command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst

			self.systemCommand(command)

			flowURL = "http://"+controller_ip+":8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ way[target][currentNode] +"/table/0/flow/2"

			command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc

			self.systemCommand(command)

		srcNode = way[target][-1]
		prevNode = way[target][-2]
		inport = linkPorts[prevNode + "::" + srcNode]
		inport = inport.split("::")[1]
		outport = hostPorts[h2]

		xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>32767</priority><flow-name>Load Balance 1</flow-name><match><in-port>' + str(inport) +'</in-port><ipv4-destination>10.0.0.1/32</ipv4-destination><ipv4-source>10.0.0.2/32</ipv4-source><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>1</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(outport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>\''

		xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>32767</priority><flow-name>Load Balance 2</flow-name><match><in-port>' + str(outport) +'</in-port><ipv4-destination>10.0.0.2/32</ipv4-destination><ipv4-source>10.0.0.1/32</ipv4-source><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>2</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(inport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>\''

		flowURL = "http://"+controller_ip+":8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ way[target][-1] +"/table/0/flow/1"

		command = 'curl --user \"admin\":\"admin\" -H \"Accept: application/xml\" -H \"Content-type: application/xml\" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst

		self.systemCommand(command)

		flowURL = "http://"+controller_ip+":8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ way[target][-1] +"/table/0/flow/2"

		command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc

		self.systemCommand(command)
		



	

	def reset(self):
		global h1,h2,h3,path1
		path1={}
		h1 = "10.0.0.1"
		h2 = "10.0.0.2"
		global target
		target=h1[-1]+":"+h2[-1]
		
		#Creating Graph
		global G
		G = nx.Graph()

		# Stores Info About H3 And H4's Switch
		global switch
		switch = {}

		# MAC of Hosts i.e. IP:MAC
		global deviceMAC
		deviceMAC = {}

		# IP of Hosts i.e. MAC:IP
		global deviceIP
		deviceIP = {}

		# Stores Switch Links To H3 and H4's Switch
		global switchLinks
		switchLinks = {}

		# Stores Host Switch Ports
		global hostPorts
		hostPorts = {}
			
		# Stores Switch To Switch Path
		global path
		path = {}
		# Stores Link Ports
		global linkPorts
		linkPorts = {}
		# Stores Final Link Rates
		global finalLinkTX
		finalLinkTX = {}
		# Store Port Key For Finding Link Rates
		global portKey
		portKey = ""
		# Statistics
		global stats
		stats = ""
		# Stores Link Cost
		#global cost
		#cost = 0

		
		 # Device Info (Switch To Which The Device Is Connected & The MAC Address Of Each Device)
		topology = "http://192.168.238.132:8181/restconf/operational/network-topology:network-topology"
		self.getResponse(topology,"topology")

		# Print Device:MAC Info
		print ("\nDevice IP & MAC\n")
		print (deviceMAC)

		# Print Switch:Device Mapping
		print ("\nSwitch:Device Mapping\n")
		print (switch)

		# Print Host:Port Mapping
		print ("\nHost:Port Mapping To Switch\n")
		print (hostPorts)

		# Print Switch:Switch Port:Port Mapping
		print ("\nSwitch:Switch Port:Port Mapping\n")
		print (linkPorts)
		num=1
		#for path in nx.all_shortest_paths(G, source=int(switch[h1].split(":",1)[1]), target=int(switch[h2].split(":",1)[1]), weight=None):
		for path in nx.all_simple_paths(G, source=int(switch[h1].split(":",1)[1]), target=int(switch[h2].split(":",1)[1])):
			a=""
			for i in range(0,len(path)):
				a+=str(path[i])

			path1[str(num)]=a
			num+=1
		return self.get_s()
			
			
	def timeover(self):#作用:避免重复发起数据传输，会报错
		global Randomly_decide_to_send_interfering_streams
		Randomly_decide_to_send_interfering_streams=True
				
	def get_s(self):#用于获取流量矩阵
		global linkPorts,switch_number,s_last
		s=np.zeros((switch_number, switch_number),dtype=np.int)
		global Randomly_decide_to_send_interfering_streams
		if Randomly_decide_to_send_interfering_streams:

			Net.sed_ganrao()
			
			Randomly_decide_to_send_interfering_streams=False
			timer_thread = threading.Timer(40, self.timeover)
			timer_thread.start()
		time.sleep(5)
		
		for t in linkPorts:
			port = linkPorts[t]
			node = t.split(":",1)[0]
			port = port.split(":",1)[0]
			port = int(port)
			stats = "http://"+controller_ip+":8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:"+str(node)+"/node-connector/openflow:"+str(node)+":"+str(port)
			tx=self.getResponse(stats,"statistics")	
			s[int(node)-1,int(t.split(":")[2])-1]=tx-s_last[int(node)-1,int(t.split(":")[2])-1]	
			s_last[int(node)-1,int(t.split(":")[2])-1]=tx

		for i in range(4):
			for j in range(4):
				if flows.objects.filter(source_switch=i,destination_switch=j).exists():
					flows.objects.filter(source_switch=i,destination_switch=j).update(flows=int(s[i][j]))
				else :
					flows1=flows(source_switch=i,destination_switch=j,flows=int(s[i][j]))
					flows1.save()

		return s


	def step(self,a):#将选出的路由路径应用到网络中(下发流表操作)
		global way
		way={}
		global path1#代表从src到dst的所有可通路径
		global target#reset()中定义了，例如1：2
		way[target]=path1[str(np.argmax(a)+1)]
		print("h1->h2本次小回合的预测路径:要经过交换机")
		print(way[target])

		r=-5
		done=True
		for i  in range(1,len(path1)+1):
			
			
			if path1[str(i)]==way[target]:
				r=get_data()
				done=False#因为成功了，所以没结束,环境可以继续
				
		if not done:
			self.pushFlowRules()#xml根据路径引导流量

			
		s_next=self.get_s()#ppo获取下一状态s
		return s_next,r,done


	
		

def normalize(s):#归一化处理
	global switch_number
	mean = np.mean(s)
	std = np.std(s)
	s=(s-mean)/std
	return s

def get_data():
	global yanshi,diubaolv,daikuan,framerate,coderate
	data=None
	Net.iperf()#测试h1h2之间的udp，并将结果保存在customs下client1.out中
	file=open("/home/windy/mininet/custom/client1.out",'r')
	while not data:
		data=file.readlines()
	if data[-1].split()[-1][-1]!=')':
		data=data[-2].split()
	else: data=data[-1].split()
	try:
		if data[-4]=='ms':
			yanshi=float(data[-5])
		else:
			yanshi=float(data[-4])
		diubaolv=re.search(r'([\d\.]+)%', data[-1])	
		if diubaolv:
	    		value = round(float(diubaolv.group(1))*0.01,2)
			diubaolv=value
		else:
	    		diubaolv=0	
		daikuan=1
		framerate,coderate=Net.get_fr_br()
		framerate=round(float(framerate),2)
		coderate=round(float(coderate),2)		
	except Exception as e:#运行出错，取最近一次的数据来“糊弄”，防止程序终端运行
		print('we use last network data!')
		print(e)
		

	w1=100
	w2=0.3
	w3=1
	w4=0.1
	print('delay: {} ms'.format(yanshi))
	#print('daikuan: {} Kbits/ses'.format(daikuan))
	print('framerate: {} fps '.format(framerate))
	print('coderate: {} Mbits/s'.format(coderate))
	print('packet_loss: {} '.format(diubaolv))
	print("reward:")

	print(w1*(1-diubaolv)+w2*framerate+w3/yanshi+w4*coderate)
	return(w1*(1-diubaolv)+w2*framerate+w3/yanshi+w4*coderate)

def database_info():
	global ep_yanshi,ep_diubaolv,ep_daikuan,ep_framerate,ep_coderate,iteration
	info=Info(iteration=iteration,delay=ep_yanshi,packet_loss=ep_diubaolv,bandwidth=ep_daikuan,frame_rate=ep_framerate,code_rate=ep_coderate)
	info.save()
def database_delete():
	flows.objects.all().delete()
	Switch.objects.all().delete()
	Info.objects.all().delete()
	Info_op.objects.all().delete()
	result.objects.all().delete()
	for i in range(1,switch_number+1):
		switchs=Switch(id_num=i,label='openflow'+str(i))
		switchs.save()





global s_last,s,iteration,ep_yanshi,ep_diubaolv,ep_daikuan,ep_framerate,ep_coderate,yanshi,diubaolv,daikuan,framerate,coderate
s_last=np.zeros((switch_number, switch_number),dtype=np.int)
env=env()#环境初始化
env.reset()
ppo = PPO()#智能体初始化
Net.databases_host()#完善数据库Host
Net.stream()#干扰流量发送
database_delete()#数据库初始化
all_ep_r = []
all_yanshi_r=[]
all_daikuan_r=[]
all_diubaolv_r=[]
all_framerate_r=[]
all_coderate_r=[]


for ep in range(EP_MAX):
    iteration=ep
    s = env.get_s()#初始化网络状态,s此时是一个switch_number*switch_number的矩阵
    global cost
    cost = 0
    s_now=s.ravel()#转化成switch_number*switch_number的一维向量
    s_now=normalize(s_now)#归一化
    buffer_s, buffer_a, buffer_r = [], [], []#缓存
    ep_r = 0
    ep_yanshi=0
    ep_daikuan=0
    ep_diubaolv=0
    ep_framerate=0
    ep_coderate=0
    for t in range(EP_LEN):    # in one episode
        a = ppo.choose_action(s_now)
        s_, r, done = env.step(a)
        s_next=s_.ravel()
        s_next=normalize(s_next)
        buffer_s.append(s_now)
        buffer_a.append(a)
        buffer_r.append(r)    # normalize reward, find to be useful
        s_now = s_next
        ep_r += r
        ep_yanshi+=yanshi
	ep_daikuan+=daikuan
	ep_diubaolv+=diubaolv
        ep_framerate+=framerate
        ep_coderate+=coderate
	print("小回合轮数:%d"%t)


        # update ppo
        if (t+1) % BATCH == 0 or t == EP_LEN-1:
            v_s_ = ppo.get_v(s_next)
            discounted_r = []
            for r in buffer_r[::-1]:
                v_s_ = r + GAMMA * v_s_
                discounted_r.append(v_s_)
            discounted_r.reverse()

            bs, ba, br = np.vstack(buffer_s), np.vstack(buffer_a), np.array(discounted_r)[:, np.newaxis]
            buffer_s, buffer_a, buffer_r = [], [], []
            ppo.update(bs, ba, br)
    database_info()
    if ep == 0: 
	all_ep_r.append(ep_r)
	all_yanshi_r.append(ep_yanshi)
	all_daikuan_r.append(ep_daikuan)
	all_diubaolv_r.append(ep_diubaolv)
	all_framerate_r.append(ep_framerate)
	all_coderate_r.append(ep_coderate)
	
    else: 
	all_ep_r.append(all_ep_r[-1]*0.9 + ep_r*0.1)
	all_yanshi_r.append(all_yanshi_r[-1]*0.9 + ep_yanshi*0.1)
	all_daikuan_r.append(all_daikuan_r[-1]*0.9 + ep_daikuan*0.1)
	all_diubaolv_r.append(all_diubaolv_r[-1]*0.9 + ep_diubaolv*0.1)
	all_framerate_r.append(all_framerate_r[-1]*0.9 + ep_framerate*0.1)
	all_coderate_r.append(all_coderate_r[-1]*0.9 + ep_coderate*0.1)
    results=result(iteration=iteration,result=all_ep_r[iteration])
    results.save()
    with open('result.txt', 'a+') as f:
    	for i in range(0, len(all_ep_r)):
    		f.write("{%d"%(i)+"} {%f"%(all_ep_r[i])+"}\n")
    with open('resultyanshi.txt', 'a+') as f:
    	for i in range(0, len(all_yanshi_r)):
    		f.write("{%d"%(i)+"} {%f"%(all_yanshi_r[i])+"}\n")
    with open('resultdaikuan.txt', 'a+') as f:
    	for i in range(0, len(all_daikuan_r)):
    		f.write("{%d"%(i)+"} {%f"%(all_daikuan_r[i])+"}\n")
    print(
        'Ep: %i' % ep,
        "|Ep_r: %i" % ep_r,
        ("|Lam: %.4f" % METHOD['lam']) if METHOD['name'] == 'kl_pen' else '',
    )
	



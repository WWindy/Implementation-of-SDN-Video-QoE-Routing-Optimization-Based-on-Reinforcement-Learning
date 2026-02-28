#  一、目标问题与意义价值
随着互联网技术的迅速发展，线上视频会议已经成为一种越来越流行的业务应用，为企业之间的协作提供了更加便捷、高效的方式。然而，尤其是在线教育、远程医疗等需要高实时性和稳定性的应用场景中，由于网络性能问题，在视频会议过程中可能会出现卡顿、延迟、画面不清晰等现象，影响了用户体验和业务效率。
本作品重点关注视频会议实时性和稳定性的问题，在网络拓扑决策上引入了面向用户QoE（Quality of Experience）的智能体NTDA（Network Topology Decision Agent），提出了基于强化学习的SDN视频QoE路由优化算法RLQR-SV（Reinforcement Learning-based QOE Routing Algorithm for SDN Video Transmission），通过优化路由策略提高视频会议的实时性和稳定性，保障用户体验。同时，该作品也对近端策略优化算法（Proximal Policy Optimization）的应用进行了探索和实践，为其在网络领域的应用提供了新思路和方法。

# 二、设计思路与方案
本项目以该SDN架构作为实验环境，采用如图（1）所示的项目框架。将应用平面中的智能体作为本项目的“芯片”，负责进行网络中的路由决策，控制平面中的SDN控制器作为本架构的“领导”，根据“芯片”的指示对转发平面下达流表更新的指令。
<img width="206" height="247" alt="image" src="https://github.com/user-attachments/assets/618b1298-be5d-47c9-bff7-0fe5f816e74c" />
项目整体运行流程如图（2）所示。首先，依据图（1）所示的架构，使用Mininet创建如图（3）所示的自定义网络拓扑结构。然后，如图（4）所示，在各主机之间使用VLC（Video Lan Client）进行视频传输，模拟实时视频通信环境。再后，设计一个基于强化学习的SDN视频QoE路由优化算法（RLQR-SV），用于代替物理网络中的路由算法等决策手段。它可通过iperf，wireshark抓包等手段实时获取网络的性能参数以及流量状态等指标，根据计算出的用户体验质量QoE参数值，决策出最优路径并发送给OpenDayLight控制器。在获取到该路径后，OpenDayLight控制器立即更新对应流表，将流量引导至该路径上，在此期间，基于强化学习的SDN视频QoE路由优化算法（RLQR-SV）根据实时网络情况不断调整策略，最终达到优化网络，提高用户QoE高质量体验的目的。
<img width="330" height="297" alt="image" src="https://github.com/user-attachments/assets/2c6a7339-47b3-4b0d-be58-28bfce5f4a56" />
<img width="371" height="244" alt="image" src="https://github.com/user-attachments/assets/c78bf1e2-02d4-4a7e-8d1c-7de27812d30f" />
<img width="369" height="329" alt="image" src="https://github.com/user-attachments/assets/fefb02d0-154b-46cc-9974-3412a363390d" />

# 三、效果分析
本项目将以网络流量大小为指标的基于负载均衡的迪杰斯特拉算法（Dijkstra-Load Balance）与我们提出的RLQR-SV算法进行对比，一次训练回合 (iteration) 包含33个步骤，相当于每运行33次流表更新后会进行一次PPO训练。区别于传统的基于跳数的迪杰斯特拉算法，我们在此基础上进行了改进，提出了基于负载均衡的迪杰斯特拉算法，该算法在每个小回合计算出各条路径上的数据包流量大小，根据最短路径原则，选取主机1与主机2之间流量最小的路径作为最终决策路径，通过流表下发应用到环境中。由图（10）-图（14）可见，在综合评估指标QoE方面，蓝色虚折线代表的Dijkstra-Load Balance算法的奖励数据的值相对于红色折线代表的RLQR-SV算法整体偏低，并且随着训练回合的增加，呈现下降趋势，而RLQR-SV算法的奖励值（QoE值）呈现上升趋势。在指标帧率 (Frame_rate) 和码率 (Code_rate) 方面，蓝色虚折线代表的Dijkstra-Load Balance算法总体变化不明显，而RLQR-SV算法随着训练回合的增加，其变化幅度大，并总体呈现上升趋势，在指标丢包率 (Packet_loss_rate) 和时延 (Time_delay) 方面，明显可以看出蓝色虚折线代表的Dijkstra-Load Balance算法总体都高于红色折线代表的RLQR-SV算法。综上结果，RLQR-SV算法各方面性能都优于Dijkstra-Load Balance算法，充分证明了RLQR-SV算法的有效性。
- 奖励（QoE）与训练回合的变化关系：
<img width="534" height="233" alt="image" src="https://github.com/user-attachments/assets/8d059854-4206-4081-80db-8b8190bb0da8" />
- 帧率与训练回合的变化关系：
<img width="514" height="232" alt="image" src="https://github.com/user-attachments/assets/024ed4d0-fd71-48aa-8b1a-d94b15bbfc0d" />
- 码率与训练回合的变化关系：
<img width="500" height="228" alt="image" src="https://github.com/user-attachments/assets/825c3997-2e1b-48cb-a5b1-6457881eff89" />
- 丢包率与训练回合的变化关系：
<img width="515" height="226" alt="image" src="https://github.com/user-attachments/assets/2affe8d6-d90a-4ffb-a106-17ebcebd3875" />
- 时延与训练回合的变化关系：
<img width="499" height="226" alt="image" src="https://github.com/user-attachments/assets/5820d886-cd66-4e54-94d7-3d363c0f52d1" />

let options = {
  data: [
    {
      type: 'host',// 节点类型
      name: 'ip:10.0.0.1',// 节点名称
      underText: '',// 节点之间连接线下方的文字
      upwardText: "",// 节点之间连接线上方的文字
    },
    {
      type: 'Switch',
      name: 's1',
      underText: '',
      upwardText: "",
    },
    {
      type: 'host',
      name: 'ip:10.0.0.2',
      underText: '',
      upwardText: "",
    },
    {
      type: 'Switch',
      name: 's2',
      underText: '',
      upwardText: "",
    },
    {
      type: 'host',
      name: 'ip:10.0.0.3',
      underText: '',
      upwardText: "",
    },
    {
      type: 'Switch',
      name: 's3',
      underText: '',
      upwardText: "",
    },
    {
      type: 'host',
      name: 'ip:10.0.0.4',
      underText: '',
      upwardText: "",
    },
    {
      type: 'Switch',
      name: 's4',
      underText: '',
      upwardText: "",
    },
    {
      type: 'host',
      name: 'ip:10.0.0.5',
      underText: '',
      upwardText: "",
    },
    {
      type: 'Switch',
      name: 's5',
      underText: '',
      upwardText: "",
    },
  ],
  edges: [
    {
      source: 1,  // 连接线起点(数值对应data数组中的元素)
      target: 0,  // s1-h1
    },
    {
      source: 1,  // 连接线起点(数值对应data数组中的元素)
      target: 3,  // s1-s2
    },
    {
      source: 1,  // 连接线起点(数值对应data数组中的元素)
      target: 5,  // 连接线终点(数值对应data数组中的元素)
    },
    {
      source: 1,  // 连接线起点(数值对应data数组中的元素)
      target: 7,  // 连接线终点(数值对应data数组中的元素)
    },
    {
      source: 1,
      target: 9,
    },
    {
      source: 3,
      target: 2,  //s2-h2
    },
    {
      source: 3,
      target: 5,
    },
    {
      source: 3,
      target: 7,
    },
    {
      source: 3,
      target: 9,
    },
    {
      source: 5,
      target: 4,
    },
    {
      source: 7,
      target: 6,
    },
    {
      source: 9,
      target: 8,  //s5-h5
    }
  ],
  path1: [//s1s2
    {
      source: 0,
      dest: 1,
      flow: 88,
    },
    {
      source: 1,
      dest: 3,
      flow: 99,
    },
    {
      source: 3,
      dest: 2,
      flow: 57,
    }
  ],
  path2: [//s1s4s2
    {
      source: 0,
      dest: 1,
      flow: 88,
    },
    {
      source: 1,
      dest: 7,
      flow: 99,
    },
    {
      source: 7,
      dest: 3,
      flow: 99,
    },
    {
      source: 3,
      dest: 2,
      flow: 57,
    }
  ],
  path3: [//s1s3s2
    {
      source: 0,
      dest: 1,
      flow: 88,
    },
    {
      source: 1,
      dest: 5,
      flow: 99,
    },
    {
      source: 5,
      dest: 3,
      flow: 99,
    },
    {
      source: 3,
      dest: 2,
      flow: 57,
    }
  ],
  path4: [//s1s5s2
    {
      source: 0,
      dest: 1,
      flow: 88,
    },
    {
      source: 1,
      dest: 7,
      flow: 99,
    },
    {
      source: 7,
      dest: 3,
      flow: 99,
    },
    {
      source: 3,
      dest: 2,
      flow: 57,
    }
  ],
}
export default options
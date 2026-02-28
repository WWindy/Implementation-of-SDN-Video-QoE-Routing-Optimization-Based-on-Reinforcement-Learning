let list = {
  nodeInfos: [
    {
      id: "node1",
      label: "主机1",
      type: "host"
    }, {
      id: "node2",
      label: "主机2",
      type: "host"
    }, {
      id: "node3",
      label: "主机3",
      type: "host"
    }, {
      id: "node4",
      label: "主机4",
      type: "host"
    }, {
      id: "node5",
      label: "主机5",
      type: "host"
    }, {
      id: "node6",
      label: "交换机1",
      type: "Switch"
    }, {
      id: "node7",
      label: "交换机2",
      type: "Switch"
    }, {
      id: "node8",
      label: "交换机3",
      type: "Switch"
    }, {
      id: "node9",
      label: "交换机4",
      type: "Switch"
    }, {
      id: "node10",
      label: "交换机5",
      type: "Switch"
    }
  ],
  edges: [
    {
      source: "node1",
      target: "node6",
    },
    {
      source: "node6",
      target: "node7",
    },
    {
      source: "node6",
      target: "node8",
    },
    {
      source: "node6",
      target: "node9",
    },
    {
      source: "node6",
      target: "node10",
    },
    {
      source: "node7",
      target: "node2",
    },
    {
      source: "node7",
      target: "node8",
    },
    {
      source: "node7",
      target: "node9",
    },
    {
      source: "node7",
      target: "node10",
    },
    {
      source: "node8",
      target: "node3",
    },
    {
      source: "node4",
      target: "node9",
    },
    {
      source: "node5",
      target: "node10",
    },
    // {
    //   source: "node6",
    //   target: "node1",
    // },
    // {
    //   source: "node7",
    //   target: "node1",
    // },
    // {
    //   source: "node8",
    //   target: "node1",
    // },
    // {
    //   source: "node9",
    //   target: "node1",
    // },
    // {
    //   source: "node10",
    //   target: "node1",
    // },
    // {
    //   source: "node7",
    //   target: "node2",
    // },
    // {
    //   source: "node8",
    //   target: "node2",
    // },
    // {
    //   source: "node9",
    //   target: "node2",
    // },
    // {
    //   source: "node10",
    //   target: "node2",
    // },
    // {
    //   source: "node8",
    //   target: "node3",
    // },
    // {
    //   source: "node9",
    //   target: "node4",
    // },
    // {
    //   source: "node10",
    //   target: "node5",
    // }
  ],
  path1: [//s1s2
    {
      source: "node1",
      dest: "node6",
      flow: 88,
    },
    {
      source: "node1",
      dest: "node6",
      flow: 88,
    },
    {
      source: "node6",
      dest: "node7",
      flow: 99,
    },
    {
      source: "node7",
      dest: "node2",
      flow: 57,
    }
  ],
  path2: [//s1s4s2
    {
      source: "node1",
      dest: "node6",
      flow: 88,
    },
    {
      source: "node6",
      dest: "node9",
      flow: 99,
    },
    {
      source: "node7",
      dest: "node9",
      flow: 99,
    },
    {
      source: "node7",
      dest: "node2",
      flow: 57,
    }
  ],
  path3: [//s1s3s2
    {
      source: "node1",
      dest: "node6",
      flow: 88,
    },
    {
      source: "node6",
      dest: "node8",
      flow: 99,
    },
    {
      source: "node8",
      dest: "node7",
      flow: 99,
    },
    {
      source: "node7",
      dest: "node2",
      flow: 57,
    }
  ],
  path4: [//s1s5s2
    {
      source: "node1",
      dest: "node6",
      flow: 88,
    },
    {
      source: "node6",
      dest: "node9",
      flow: 99,
    },
    {
      source: "node9",
      dest: "node7",
      flow: 99,
    },
    {
      source: "node7",
      dest: "node2",
      flow: 57,
    }
  ],
}
export default list
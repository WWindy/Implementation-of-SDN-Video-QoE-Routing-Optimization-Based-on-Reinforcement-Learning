<template>
  <div>
    <!-- show the topo -->
    <svg width="1800" height="700">
      <g />
    </svg>
  </div>
</template>

<script>
import list from "../../jsondata/flowPath";
import dagreD3 from "dagre-d3";
import * as d3 from "d3";
import $ from "jquery";
export default {
  data() {
    return {

    };
  },
  methods: {
    turnDir(dir) {
      this.direction = dir;
      this.drawTopo();
    },
    drawTopo() {
      //获取D3
      var g = new dagreD3.graphlib.Graph()
        .setGraph({
          rankdir: this.direction,
          edgesep: 50,
          ranksep: 50,
        })
        .setDefaultEdgeLabel(function() {
          return {};
        });

      function drawNode(arr) {
        // 添加节点(设置节点的特性)
        arr.forEach((item) => {
          g.setNode(item.id, {
            labelType: "html",
            label: `<i class="${item.type} }"><b>${item.label}</b></i>`,
          });
        });
      }
      drawNode(list.nodeInfos);

      // 链接关系(连线的属性)
      function drawLine(arr, color, opacity) {
        arr.forEach((item, index) => {
          g.setEdge(item.source, item.target, {
            lineInterpolate: "basis",
            class: `${item.source}-${item.target}`,
            style: `stroke: ${color}; fill: none;opacity:${opacity};marker-end:none`,
            id: "status" + index,
          });
        });
      }
      drawLine(list.edges, "#red", 1);

      //绘制图形
      var svg = d3.select("svg"),
        inner = svg.select("g");

      //缩放
      var zoom = d3.zoom().on("zoom", function() {
        inner.attr("transform", d3.event.transform);
      });
      svg.call(zoom);

      var render = new dagreD3.render();
      render(inner, g);

      //鼠标悬浮事件
      inner
        .selectAll("g.node")
        .on("mouseover", (e) => {
          // 先获取所有的线段,并将这些线段都设置透明度为0.2
          $(`g.edgePath`).attr("style", "opacity:0.2");
          console.log($(`g.edgePath`));
          // 当前的节点名字为e,将所有与e有关的线段添加类名active,进行高亮显示
          list.edges.forEach((item) => {
            $(`.${e}-${item.target}`).addClass("active");
            $(`.${item.target}-${e}`).addClass("active");
            $(`.${e}-${item.source}`).addClass("active");
            $(`.${item.source}-${e}`).addClass("active");
          });
        })
        .on("click ", () => {
          return false;
        })
        .on("mouseout", () => {
          drawLine(list.edges, "#4c7fe5", 1);
          var render = new dagreD3.render();
          render(inner, g);
        });

      var initialScale = 1;
      svg.call(
        zoom.transform,
        d3.zoomIdentity
          .translate(
            (svg.attr("width") - g.graph().width * initialScale) / 2,
            50
          )
          .scale(initialScale)
      );
      svg.attr("height", g.graph().height * initialScale + 100);
      var mpath = [list.path1, list.path2, list.path3, list.path4];
      console.log(mpath);
      
      //  show the flow's path
      function showflow() {
        let i, s;
        setInterval(() => {
          i = Math.floor(Math.random() * 4);
          s = mpath[i];
          $(`g.edgePath`).attr("style", "opacity:0.5");
          // set the highlight
          list.edges.forEach((item) => {
            if (item.source == s[0].source && item.target == s[0].dest) {
              // console.log($(`.${s[0].source}-${s[0].dest}`)+"!!!!!!!1");
              $(`.${s[0].source}-${s[0].dest}`).addClass("active");
            }
            $(`.${s[1].source}-${s[1].dest}`).addClass("active");
            $(`.${s[2].source}-${s[2].dest}`).addClass("active");
            $(`.${s[3].source}-${s[3].dest}`).addClass("active");
          });
          // clear the highlight
          setTimeout(() => {
            $(`.${s[0].source}-${s[0].dest}`).removeClass("active");
            $(`.${s[1].source}-${s[1].dest}`).removeClass("active");
            $(`.${s[2].source}-${s[2].dest}`).removeClass("active");
            $(`.${s[3].source}-${s[3].dest}`).removeClass("active");
          }, 2000);
        }, 3000);
      }

      showflow();
    },
  },

  mounted() {
    this.drawTopo();
  },
};
</script>

<style lang="less">
svg {
  font-size: 14px;
  border: 1px solid #000;
}

foreignObject {
  width: 50px;
  height: 63px;
  background-color: transparent;
}

.node circle,
.node ellipse,
.node rect {
  fill: transparent;
  stroke-width: 0px;
  stroke: red;
}

.edgePath path {
  width: 0;
  stroke: #4c7fe5;
  fill: rgb(39, 86, 203);
  stroke-width: 2.5px;
}

.host,
.Switch {
  display: inline-block;
  width: 40px;
  height: 40px;
  background-size: contain;
  position: relative;
  overflow: visible;
  background-repeat: no-repeat;

  b {
    position: absolute;
    bottom: -25px;
    left: 50%;
    transform: translateX(-50%);
    font-style: normal;
    color: #fff;
  }
}

.active {
  stroke-width: 2px;
  opacity: 1 !important;

  path {
    stroke: #ec725a !important;
  }
}


.host {
  background-image: url("../../assets/host.png");
}

.Switch {
  background-image: url("../../assets/Switch.png");
}
</style>

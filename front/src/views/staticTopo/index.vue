<template>
  <div style="height: 100%">
    <svg id="topo" width="1800" height="1000"></svg>
  </div>
</template>

<script>
import options from "../../jsondata/staticTopo";
import * as d3 from "d3";
export default {
  name: "topo",
  data() {
    return {

    };
  },
  methods: {

  },
  mounted() {
    const fontSize = 10;
    const symbolSize = 40;
    const padding = 10;
    const that = this;
    class Topo {
      constructor(svg, option) {
        this.data = option.data;
        this.edges = option.edges;
        this.svg = d3.select(svg);
      }

      //初始化节点位置
      initPosition() {
        let width = this.svg.attr("width");
        let height = this.svg.attr("height");
        let points = this.getVertices(this.data.length);
        this.data.forEach((item, i) => {
          item.x = points[i].x + width / 4;
          item.y = points[i].y + height / 9;
        });
      }

      //根据节点的个数，生成矩形阵列(即配置节点的摆放位置),返回的points为节点的定位坐标[{x:..,y:...},...]
      getVertices(n) {
        if (typeof n !== "number") return;
        var i = 0;
        var j = 0;
        var k = 0;
        var points = [];
        while (k < n) {
          points.push({
            x: 100 + 300 * i,
            y: 100 + 300 * j,
          });
          if (i < 2) {
            i++;
          } else {
            i = 0;
            j++;
          }
          k++;
        }
        return points;
      }

      // 计算两点的中心点(用于确认摆放在连接线上的文字的位置)
      getCenter(x1, y1, x2, y2) {
        return [(x1 + x2) / 2, (y1 + y2) / 2];
      }

      // 计算两点角度
      getAngle(x1, y1, x2, y2) {
        var x = Math.abs(x1 - x2);
        var y = Math.abs(y1 - y2);
        var z = Math.sqrt(x * x + y * y);
        return Math.round((Math.asin(y / z) / Math.PI) * 180);
      }

      // 初始化缩放器
      initZoom() {
        let self = this;
        let zoom = d3
          .zoom()
          .scaleExtent([0.7, 3])
          .on("zoom", function() {
            self.onZoom(this);
          });
        this.svg.call(zoom);
      }

      // 初始化图标库
      initDefineSymbol() {
        // defs用于预定义一个元素使其能够在SVG图像中重复使用，我们defs标签中的g元素必须在<g>元素上设置一个ID，通过ID来引用它。
        let defs = this.container.append("svg:defs");
        // 向defs中添加交换机
        let Switch = defs
          .append("g")
          .attr("id", "Switch")
          .attr("transform", "scale(0.042)");

        Switch.append("path")
          .attr(
            "d",
            "M0 373.14949l650.250205 379.752843v271.097667L0 644.367218V373.269551z"
          )
          .attr("style", "fill:#B8D9F6");

        Switch.append("path")
          .attr(
            "d",
            "M1300.620471 373.14949L650.250205 752.902333v271.097667l650.250205-379.632782V373.14949"
          )
          .attr("style", "fill:#99C9F2");

        Switch.append("path")
          .attr(
            "d",
            "M1305.302849 373.269551L651.330754 0 4.9225 373.14949l645.327705 378.672294z"
          )
          .attr("style", "fill:#E0EFFB");

        Switch.append("path")
          .attr(
            "d",
            "M919.186775 511.459726l-27.614023-59.069997a9.364756 9.364756 0 0 0-3.962012-4.082073 24.012194 24.012194 0 0 0-21.851096 0 24.012194 24.012194 0 0 1-21.851097 0l-81.641458-47.18396c-4.442256-2.52128-5.642866-6.363231-3.481768-9.724939a42.021339 42.021339 0 0 0 0-49.465119c-2.281158-3.241646-0.840427-7.083597 3.361707-9.484816l80.440849-46.823778a24.012194 24.012194 0 0 1 21.851096 0c8.404268 4.9225 22.811584 2.641341 25.813108-4.082073l26.893657-58.949935c1.560793-3.361707 0-6.483292-4.082073-8.64439a24.012194 24.012194 0 0 0-14.88756-2.281159L796.844648 228.11584c-12.006097 1.800915-15.247743 10.085121-6.843476 15.007621a6.723414 6.723414 0 0 1 0 12.726463l-79.960605 46.463595a24.012194 24.012194 0 0 1-16.568413 1.920975 197.500293 197.500293 0 0 0-86.924141 0 24.012194 24.012194 0 0 1-16.688475-1.920975l-80.56091-46.463595a6.723414 6.723414 0 0 1 0-12.726463c6.363231-3.72189 5.642866-9.364756 0-12.726463a20.050182 20.050182 0 0 0-6.963536-2.281158l-101.931762-15.848048c-12.006097-1.800915-21.971157 4.322195-18.849572 10.925548l27.614023 59.069997a9.484817 9.484817 0 0 0 3.962011 3.962012 24.012194 24.012194 0 0 0 21.971158 0 24.012194 24.012194 0 0 1 21.851096 0l81.041154 46.823778c4.322195 2.52128 5.642866 6.24317 3.481768 9.484816a41.901278 41.901278 0 0 0 0.840427 49.58518c2.281158 3.361707 0.960488 7.083597-3.361708 9.604877l-81.161214 47.183961a24.012194 24.012194 0 0 1-21.851097 0c-8.404268-4.9225-22.811584-2.641341-25.813108 4.082073l-27.133779 58.589753c-1.560793 3.361707 0 6.483292 4.082073 8.644389a24.012194 24.012194 0 0 0 14.88756 2.281159L504.256068 506.657287c12.006097-1.800915 15.247743-10.085121 6.843475-15.007621a6.723414 6.723414 0 0 1 0-12.726463l81.641458-48.024387a24.012194 24.012194 0 0 1 16.448353-2.041037 197.260171 197.260171 0 0 0 84.042678 0 24.012194 24.012194 0 0 1 16.568414 2.041037l82.121702 48.024387a6.723414 6.723414 0 0 1 0 12.606402c-6.363231 3.72189-5.642866 9.364756 0 12.726463a20.050182 20.050182 0 0 0 6.963536 2.281158L900.457263 522.505335c11.405792 1.800915 21.851096-4.322195 18.729512-11.045609z m-268.93657-116.339079c-24.012194 0-44.422558-12.006097-44.422558-27.974205s19.930121-27.974206 44.422558-27.974206 44.422558 12.006097 44.422559 27.974206-19.81006 27.974206-44.422559 27.974205z"
          )
          .attr("style", "fill:#5CA8EA");

        // 向defs中添加主机
        let host = defs
          .append("g")
          .attr("id", "host")
          .attr("transform", "scale(0.042)");

        host
          .append("path")
          .attr(
            "d",
            "M377.889841 640.783354v17.964912c0 63.71277 94.002448 115.414117 210.565483 115.414117S799.020808 722.461036 799.020808 658.748266v-17.964912z"
          )
          .attr("style", "fill:#99C9F2");

        host
          .append("path")
          .attr(
            "d",
            "M377.889841 640.783354a210.565483 115.414117 0 1 0 421.130967 0 210.565483 115.414117 0 1 0-421.130967 0Z"
          )
          .attr("style", "fill:#E0EFFB");

        host
          .append("path")
          .attr(
            "d",
            "M945.56018 345.197878a26.425133 26.425133 0 0 0-13.160343-22.769481L387.081191 3.655651a26.425133 26.425133 0 0 0-39.794369 22.873929L348.853529 432.933497a26.425133 26.425133 0 0 0 13.160343 22.769481l176.515708 103.193799v74.366381l55.356997 32.900857V591.170951l313.341493 183.200326A26.425133 26.425133 0 0 0 946.709098 752.019584z"
          )
          .attr("style", "fill:#99C9F2");

        host
          .append("path")
          .attr(
            "d",
            "M913.912689 359.298246a26.425133 26.425133 0 0 0-13.160343-22.769482L355.433701 17.756018a26.425133 26.425133 0 0 0-39.79437 22.873929l1.148919 406.403917a26.425133 26.425133 0 0 0 13.055895 22.978376l201.896369 118.025296v41.778865l55.356997 32.900857v-41.778866L875.162791 788.576091a26.425133 26.425133 0 0 0 39.794369-22.873929z"
          )
          .attr("style", "fill:#E0EFFB");

        host
          .append("path")
          .attr(
            "d",
            "M845.604243 734.054672l-483.172582-282.007344a23.500612 23.500612 0 0 1-11.593636-20.158303l-1.044471-338.931049a23.500612 23.500612 0 0 1 35.303141-20.26275L868.269278 355.120359a23.500612 23.500612 0 0 1 11.593635 20.158303l1.044472 338.931048a23.500612 23.500612 0 0 1-35.303142 19.844962z"
          )
          .attr("style", "fill:#5CA8EA");

        host
          .append("path")
          .attr(
            "d",
            "M77.290902 792.440636l353.449204 205.969809V1023.582211L77.290902 817.925745v-25.485109z"
          )
          .attr("style", "fill:#B8D9F6");

        host
          .append("path")
          .attr(
            "d",
            "M585.530804 909.421461l-154.790698 88.988984V1023.582211l154.790698-90.346797z"
          )
          .attr("style", "fill:#99C9F2");

        host
          .append("path")
          .attr(
            "d",
            "M585.530804 909.421461l-355.120359-203.045288L77.290902 792.440636l353.449204 205.447573z"
          )
          .attr("style", "fill:#E0EFFB");

        host
          .append("path")
          .attr(
            "d",
            "M517.849041 898.245614L240.646267 739.27703l-11.906977 8.46022L504.688698 908.69033z"
          )
          .attr("style", "fill:#5CA8EA");
      }

      //初始化链接线
      initLink() {
        this.drawLinkLine();
        this.drawLinkText();
      }

      //初始化节点
      initNode() {
        var self = this;
        //节点容器
        this.nodes = this.container
          .selectAll(".node")
          .data(this.data)
          .enter()
          .append("g")
          .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
          })
          .call(
            d3
              .drag()
              // 给每一个节点添加拖拽事件
              .on("drag", function(d) {
                self.onDrag(this, d);
              })
          )

        //节点图标
        this.drawNodeSymbol();
        //节点标题
        this.drawNodeTitle();
      }

      //绘制节点图标
      drawNodeSymbol() {
        // 在<defs>元素中定义的图形不会直接显示在SVG图像上。要显示它们需要使用<use>元素来引入它们
        // <use>元素通过xlink:href属性来引入<g>元素。注意在ID前面要添加一个#。
        // 绘制host图标
        this.nodes
          .filter((item) => item.type == "host")
          .append("use")
          .attr("xlink:href", "#host")
          .attr("x", function() {
            return -this.getBBox().width / 2;
          })
          .attr("y", function() {
            return -this.getBBox().height / 2;
          });

        // 绘制Switch图标
        this.nodes
          .filter((item) => item.type == "Switch")
          .append("use")
          .attr("xlink:href", "#Switch")
          .attr("x", function() {
            return -this.getBBox().width / 2;
          })
          .attr("y", function() {
            return -this.getBBox().height / 2;
          });
      }

      //画节点标题
      drawNodeTitle() {
        //节点标题
        this.nodes
          .append("text")
          .attr("class", "node-title")
          .text(function(d) {
            return d.name;
          })
          .attr("dy", symbolSize);
      }

      // 画节点链接线
      drawLinkLine() {
        let data = this.data;
        if (this.lineGroup) {
          this.lineGroup
            .selectAll(".link")
            .attr("d", (link) => genLinkPath(link));
        } else {
          this.lineGroup = this.container.append("g");
          this.lineGroup
            .selectAll(".link")
            .data(this.edges)
            .enter()
            .append("path")
            .attr("class", "link")
            .attr("d", (link) => genLinkPath(link))
            .attr("id", (link, i) => "link-" + i);
        }

        // 确认连接线的路径
        function genLinkPath(d) {
          let sx = data[d.source].x;
          let tx = data[d.target].x;
          let sy = data[d.source].y;
          let ty = data[d.target].y;
          return "M" + sx + "," + sy + " L" + tx + "," + ty;
        }
      }

      //画节点链接线文字
      drawLinkText() {
        let data = this.data;
        let self = this;
        if (this.lineTextGroup) {
          this.lineTexts.attr("transform", getTransform);
        } else {
          this.lineTextGroup = this.container.append("g");

          this.lineTexts = this.lineTextGroup
            .selectAll(".linetext")
            .data(this.edges)
            .enter()
            .append("text")
            .attr("dy", -2)
            .attr("transform", getTransform)
            .on("click", () => {
              alert();
            });

          this.lineTexts
            .append("tspan")
            .text((d) => this.data[d.source].upwardText);

          this.lineTexts
            .append("tspan")
            .text((d) => this.data[d.source].underText)
            .attr("dy", "1em")
            .attr("dx", function() {
              return -this.getBBox().width / 2;
            });
        }

        function getTransform(link) {
          let s = data[link.source];
          let t = data[link.target];
          let p = self.getCenter(s.x, s.y, t.x, t.y);
          let angle = self.getAngle(s.x, s.y, t.x, t.y);
          if ((s.x > t.x && s.y < t.y) || (s.x < t.x && s.y > t.y)) {
            angle = -angle;
          }
          return "translate(" + p[0] + "," + p[1] + ") rotate(" + angle + ")";
        }
      }

      // 更新视图(图标位置和连接线)
      update() {
        this.drawLinkLine();
        this.drawLinkText();
        let data = this.data;
        if (this.lineGroup) {
          this.lineGroup
            .selectAll(".link")
            .attr("d", (link) => genLinkPath(link));
        } else {
          this.lineGroup = this.container.append("g");
          this.lineGroup
            .selectAll(".link")
            .data(this.edges)
            .enter()
            .append("path")
            .attr("class", "link")
            .attr("d", (link) => genLinkPath(link))
            .attr("id", (link, i) => "link-" + i);
        }
      }

      //拖拽方法
      onDrag(ele, d) {
        console.log("触发拖拽onDrag");
        d.x = d3.event.x;
        d.y = d3.event.y;
        d3.select(ele).attr(
          "transform",
          "translate(" + d3.event.x + "," + d3.event.y + ")"
        );
        this.update();
      }

      //缩放方法
      onZoom(ele) {
        this.width = this.svg.attr("width");
        var transform = d3.zoomTransform(ele);
        this.scale = transform.k;
        // this.scale>1则为放大, <1为缩小
        this.container.attr(
          "transform",
          "translate(" +
            transform.x +
            "," +
            transform.y +
            ")scale(" +
            transform.k +
            ")"
        );
      }

      //主渲染方法
      render() {
        this.scale = 1;
        // 操作svg画布
        this.container = this.svg
          .append("g")
          .attr("transform", "scale(" + this.scale + ")");
        // 执行类中定义的方法
        // 1.获取所有节点位置数据
        this.initPosition();
        // 2.初始化图标数据
        this.initDefineSymbol();
        // 3.初始化连接线的信息
        this.initLink();
        // 4.初始化节点
        this.initNode();
        // 5.初始化缩放
        this.initZoom();
      }
    }

    let t = new Topo("#topo", options);
    t.render();
  },
};
</script>

<style>
#topo {
  border: 1px solid #ccc;
  user-select: none;
}

#topo text {
  font-size: 16px;
  /*和js里保持一致*/
  fill: #fff;
  text-anchor: middle;
}

#topo .node-other {
  text-anchor: start;
}

#topo .link {
  stroke: rgb(238, 65, 97);
  stroke-width: 3;
}

#topo .node-title {
  font-size: 14px;
}

#topo .node-code text {
  fill: #fff;
}

#topo .node-bg {
  fill: #fff;
}

.active,
.active2 {
  stroke-width: 2px;
  opacity: 1 !important;

  path {
    stroke: #315dcc !important;
  }
}

.active2 {
  path {
    stroke: green !important;
  }
}
</style>

import Vue from "vue"
import VueRouter from "vue-router"
import flowPath from "../views/flowPath/index.vue"
import staticTopo from "../views/staticTopo/index.vue"
Vue.use(VueRouter)
export default new VueRouter({
  routes: [
    {
      path: '/staticTopo',
      name: "staticTopo",
      component: staticTopo
    },
    {
      path: '/flowPath',
      name: "flowPath",
      component: flowPath
    },
  ]
})
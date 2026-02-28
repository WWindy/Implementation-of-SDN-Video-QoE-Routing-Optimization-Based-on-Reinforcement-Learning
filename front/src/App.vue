<template>
  <div id="app">
    <button>
      <h1>
        <router-link class="links" to="staticTopo">拓扑展示</router-link>
      </h1>
    </button>
    &nbsp;
    <button>
      <h1>
        <router-link class="links" to="flowPath">流量路径</router-link>
      </h1>
    </button>
    <br />
    <br />
    <br />
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App'
}
</script>

<style>

body {
  background-color: #2c3e50;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  height: 100%;
  background-color: #2c3e50;
}
.links {
  text-decoration: none;
  padding: 20px;
}
button {
  margin: 0 40px;
}
</style>

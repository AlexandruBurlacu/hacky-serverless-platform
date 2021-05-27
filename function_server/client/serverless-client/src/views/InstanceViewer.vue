<template>
  <div id="instanceViewer">
    <ServerlessInstancePage instance_id=""/>
  </div>
</template>


<script>
import ServerlessInstancePage from '@/components/ServerlessInstances.vue'

// https://vuejs.org/v2/guide/

export default {
  name: 'InstanceViewer',
  components: {
    ServerlessInstancePage
  }
}

</script>

<style>
#instanceViewer {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
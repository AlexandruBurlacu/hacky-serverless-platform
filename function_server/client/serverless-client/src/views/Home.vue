<template>
  <div id="home">
    <ServerlessSubmissions msg="Welcome to a hacky Serverless Platform"/>

    <Editor/>

    <TriggerInstances/>
  </div>
</template>


<script>
import ServerlessSubmissions from '@/components/ServerlessSubmissions.vue'
import Editor from '@/components/Editor.vue'
import TriggerInstances from '@/components/TriggerInstances.vue'

// https://vuejs.org/v2/guide/

export default {
  name: 'Home',
  components: {
    ServerlessSubmissions,
    Editor,
    TriggerInstances
  }
}

</script>

<style>
#home {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
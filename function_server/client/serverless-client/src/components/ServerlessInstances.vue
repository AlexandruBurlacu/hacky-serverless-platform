<template>
  <div class="container">
    <h3>Serverless Instances Page (InstanceID {{ this.$route.params.id }})</h3>
    <!-- <h5>Instances status is {{ instance.status }}</h5> -->
    <!-- <table class="table">
      <thead>
        <tr>
          <th scope="col">Output logs</th>
          <th scope="col">Error logs</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="instance in instances.serverless_ids" v-bind:key="instance.serverless_ids">
          <th scope="row">{{ instance.outputs }}</th>
          <td>{{ instance.outputs }}</td>
        </tr>
      </tbody>
    </table> -->
    <div><p>Output logs (stdout)</p>
      {{ instance.outputs }}
    </div>
    <br>
    <div><p>Error logs (stderr)</p>
      {{ instance.stderr }}
    </div>
  </div>
</template>


<script>
  import axios from 'axios';

  export default {
    name: 'ServerlessInstancePage',
    data: () => {
      return {
        instance: null
      };
    },
    created: function() {
      axios.get(`http://localhost:7000/serverless/instance/${this.$route.params.id}/logs`)
      .then(res => {
        this.instance = res.data;
      })
    }
  }
</script>

<style>
  h3 {
    margin-bottom: 5%;
  }
</style>

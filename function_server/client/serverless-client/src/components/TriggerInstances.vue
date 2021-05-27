<template>
  <div class="container">
    <h3>Serverless Instance Trigger Page</h3>
    <form>
      <div class="form-group">
        <label for="input-data">Input Data</label>
        <input type="text" class="form-control" id="input-data" v-model="input_data">
      </div>
      <div class="form-group">
        <label for="event-type">Event Type (which will trigger the code)</label>
        <input type="text" class="form-control" id="event-type" v-model="event_type">
      </div>
      <button type="button" class="btn btn-primary" v-on:click="sendCode">Trigger serverless code</button>
    </form>
    

    <div v-for="instance in instances" v-bind:key="instance">
      <div class="alert alert-success" role="alert" ref="alert">
        Code triggered: Instance ID: <a :href="`/instances/${instance}`">{{ instance }}</a>
      </div>
    </div>

  </div>
</template>



<script>
  import axios from 'axios';

  export default {
    name: 'TriggerInstances',
    data: () => {
      return {
        input_data: "",
        event_type: "any",
        instances: null
      };
    },
    methods: {
      sendCode() {
        console.log(this.input_data)
        console.log(this.event_type)
        axios.post("http://localhost:7000/serverless/instance",
                    {event_type: this.event_type, input_data: this.input_data}, {
                      headers: {
                        "Content-Type": "application/json"
                      }
                    })
        .then((response) => {
          this.instances = response.data.instance_ids;
        })
        .catch(console.error);
      }
    }
  }
</script>

<style>
  h3 {
    margin-bottom: 5%;
  }
</style>

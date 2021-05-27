<template>
  <div class="container-fluid">
    <h3>Serverless Submissions Page says: "{{ msg }}"</h3>
    <h5>Submissions status is {{ submissions.status }}</h5>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Id</th>
          <th scope="col">Triggering Event</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="submission in submissions.serverless_ids" v-bind:key="submission.serverless_ids">
          <th scope="row">{{ submission }}</th>
          <td>{{ submission_events[submission] }}</td>
          <td>
            <button type="button" class="btn btn-primary" v-on:click="deleteSubmission(submission)">Delete it?</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>



<script>
  import axios from 'axios';

  export default {
    name: 'ServerlessSubmissions',
    data: () => {
      return {
        submissions: null,
        submission_events: {}
      };
    },
    created: function() {
      axios.get('http://localhost:7000/serverless')
      .then(res => {
        this.submissions = res.data;
      })
    },
    // watch: {
    //   submissions: function(oldVal, newVal) {
    //     console.log(newVal)
    //     console.log(oldVal)
    //     oldVal.forEach(sub => {
    //       this.getSubmissionEvent(sub);
    //     })
    //   },
    // },
    props: {
      msg: String
    },
    methods: {
      deleteSubmission(sub) {
        // console.log(`Deleting ${sub}`)
        axios.delete(`http://localhost:7000/serverless/${sub}`,
                    {
                      headers: {
                        "Content-Type": "application/json"
                      }
                    })
        // .then(console.log)
        .catch(console.error);
      },
      getSubmissionEvent(sub) {
        console.log(`Getting Summary of ${sub}`);
        var vm = this;
        axios.get(`http://localhost:7000/serverless/${sub}`,
                    {
                      headers: {
                        "Content-Type": "application/json"
                      }
                    })    
        .then((res) => {
          console.log(res.data.serverless.event_type);
          vm._submission_events[sub] = res.data.serverless.event_type;
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

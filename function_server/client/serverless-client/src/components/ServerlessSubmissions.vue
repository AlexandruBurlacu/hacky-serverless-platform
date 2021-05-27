<template>
  <div class="container">
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
          <td >{{ submission.split(":")[0] }}</td>
          <td>
            <button type="button" class="btn btn-danger" v-on:click="deleteSubmission(submission)">Delete it?</button>
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
    props: {
      instance_id: String
    },
    methods: {
      deleteSubmission(sub) {
        axios.delete(`http://localhost:7000/serverless/${sub}`,
                    {
                      headers: {
                        "Content-Type": "application/json"
                      }
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

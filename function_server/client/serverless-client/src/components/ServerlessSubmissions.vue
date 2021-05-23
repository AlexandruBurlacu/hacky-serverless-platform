<template>
  <div class="container">
    <h3> ServerlessSubmissions Page says: "{{ msg }}"</h3>
    <h5>Submissions status is {{ submissions.status }}</h5>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Id</th>
          <!-- <th scope="col">Name</th>
          <th scope="col">City</th>
          <th scope="col">Email</th> -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="submission in submissions.serverless_ids" v-bind:key="submission.serverless_ids">
          <th scope="row">{{ submission }}</th>
          <!-- <td>{{ submission.name }}</td>
          <td>{{ submission.address.city }}</td>
          <td>{{ submission.email }}</td> -->
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
      };
    },
    created: function() {
      axios.get('http://localhost:7000/serverless')
      .then(res => {
        this.submissions = res.data;
      })
    },
    props: {
      msg: String
    }
  }
</script>

<style>
  h3 {
    margin-bottom: 5%;
  }
</style>

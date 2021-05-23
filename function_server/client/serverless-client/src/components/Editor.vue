<template>
  <div>
    <prism-editor class="serverless-editor" v-model="code" :highlight="highlighter" line-numbers></prism-editor>
    <button type="button" class="btn btn-primary" v-on:click="sendCode">Submit serverless code</button>
  </div>
</template>

<script>
  // import Prism Editor
  import { PrismEditor } from 'vue-prism-editor';
  import 'vue-prism-editor/dist/prismeditor.min.css'; // import the styles somewhere

  // import highlighting library (you can use any library you want just return html string)
  import { highlight, languages } from 'prismjs/components/prism-core';
  import 'prismjs/components/prism-clike';
  import 'prismjs/components/prism-python';
  import 'prismjs/themes/prism-tomorrow.css'; // import syntax highlighting styles
  import axios from 'axios';

  export default {
    name: 'Editor',
    components: {
      PrismEditor,
    },
    data: () => ({ code: '\n\n\n' }),
    methods: {
      highlighter(code) {
        return highlight(code, languages.python); // languages.<insert language> to return html with markup
      },
      sendCode() {
        console.log(this.code)
        axios.post("http://localhost:7000/serverless",
                    {event_type: "any", code: this.code}, {
                      headers: {
                        "Content-Type": "application/json"
                      }
                    })
        .then(console.log)
        .catch(console.error);
      }
    },
  };
</script>

<style>
  /* required class */
  .serverless-editor {
    /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
    background: #6e6e6e;
    color: rgb(255, 255, 255);

    /* you must provide font-family font-size line-height. Example: */
    font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
    font-size: 14px;
    line-height: 1.5;
    padding: 5px;
  }

  /* optional class for removing the outline */
  .prism-editor__textarea:focus {
    outline: none;
  }
</style>
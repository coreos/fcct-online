<template>
<div id="container" class="col-lg-12 col-md-12 col-sm-12">
  <form id="validate">
    <div class="row">
      <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
        <h4>Enter Fedora CoreOS Config:</h4>
        <div class="co-p-validate-wrapper">
          <div class="co-p-validate-lines"></div>
          <!-- eslint-disable-next-line -->
          <textarea v-model="fcc_config" id="validate-config" wrap="off" spellcheck="false" autofocus="" rows="40"></textarea>
        </div>
      </div>
      <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
        <h4>Transpiled Ignition Config:</h4>
        <!-- eslint-disable-next-line -->
        <textarea readonly v-model="ignition_config" id="validate-results" wrap="off" spellcheck="false" autofocus="" rows="40"></textarea>
      </div>
    </div>
    <!-- eslint-disable-next-line -->
    <input type="submit" id="validate-submit" class="btn btn-primary" value="Transpile" data-category="Validator" v-on:click="submit">
  </form>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Validator',
  data() {
    return {
      fcc_config: '',
      ignition_config: '',
    };
  },
  methods: {
    cleanIgnitionBox() {
      this.ignition_config = '';
    },
    convertFccToUrl() {
      const replacedString = this.fcc_config.replace(/\n/g, '\\n');
      return encodeURI(replacedString);
    },
    toIgnitionConfig() {
      const urlConfig = this.convertFccToUrl();
      const path = 'http://127.0.0.1:5000/config/'.concat(urlConfig);
      axios.get(path)
        .then((res) => {
          try {
            this.ignition_config = JSON.parse(res.data.ignition_config);
          } catch (err) {
            this.ignition_config = res.data.ignition_config;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    submit(e) {
      e.preventDefault();
      this.cleanIgnitionBox();
      this.toIgnitionConfig();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#validate-config {
  width: 45vw;
  position: relative;
  background: transparent;
  border: 0px;
  font-size: 10pt;
  font-family: monospace;
  line-height: 14px !important;
  box-shadow: 0 0 3px rgba(153,153,153,.75)
}
#validate-results {
  width: 45vw;
  position: relative;
  background: transparent;
  border: 0px;
  font-size: 10pt;
  font-family: monospace;
  line-height: 14px !important;
  box-shadow: 0 0 3px rgba(153,153,153,.75)
}
#validate-submit {
  margin-top: 0.5em;
}
#container {
  overflow: auto;
}
</style>

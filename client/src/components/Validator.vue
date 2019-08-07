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
    <!-- eslint-disable-next-line -->
    <button type="button" id="generate-url" class="btn btn-secondary" v-on:click="showURL">Generate URL From FCC</button>
    <!-- eslint-disable-next-line -->
    <textarea readonly v-if="visible" v-model="encoded_url" id="encoded-url-box" wrap="off" spellcheck="false" autofocus="" rows="3"></textarea>
  </form>
</div>
</template>

<script>
import axios from 'axios';

const serverURL = '/config/';
const clientURL = window.location.origin.concat('/');

export default {
  name: 'Validator',

  data() {
    return {
      fcc_config: '',
      ignition_config: '',
      encoded_url: '',
      visible: false,
    };
  },

  methods: {
    cleanIgnitionBox() {
      this.ignition_config = '';
    },

    convertFccToUrl() {
      return clientURL.concat(encodeURIComponent(this.fcc_config));
    },

    toIgnitionConfig() {
      this.encoded_url = this.convertFccToUrl();
      const postData = { config_string: this.fcc_config };
      axios.post(serverURL, postData)
        .then((res) => {
          try {
            if (res.data.success) {
              this.ignition_config = JSON.stringify(res.data.message, null, 2);
            } else {
              this.ignition_config = res.data.message;
            }
          } catch (err) {
            this.ignition_config = '';
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

    showURL() {
      // eslint-disable-next-line
      this.visible = this.fcc_config ? true : false;
      this.encoded_url = this.convertFccToUrl();
    },
  },

  created() {
    if (this.$route.params.fcc_config) {
      this.fcc_config = this.$route.params.fcc_config;
      this.encoded_url = this.convertFccToUrl();
      this.showURL();
      this.toIgnitionConfig();
    }
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
  box-shadow: 0 0 3px rgba(153,153,153,.75);
  resize: none;
}
#validate-results {
  width: 45vw;
  position: relative;
  background: transparent;
  border: 0px;
  font-size: 10pt;
  font-family: monospace;
  line-height: 14px !important;
  box-shadow: 0 0 3px rgba(153,153,153,.75);
  resize: none;
}
#validate-submit {
  margin-top: 0.5em;
  margin-bottom: 1em;
}
#container {
  overflow: auto;
}
#generate-url {
  margin-top: 0.5em;
  margin-left: 0.9em;
  margin-bottom: 1em;
}
#encoded-url-box {
  width: 95vw;
  position: relative;
  background: transparent;
  border: 0px;
  font-size: 10pt;
  font-family: monospace;
  line-height: 14px !important;
  box-shadow: 0 0 3px rgba(153,153,153,.75);
  resize: none;
}
</style>

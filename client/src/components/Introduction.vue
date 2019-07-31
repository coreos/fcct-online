<template>
<div id="intro" class="col-lg-12 col-md-12 col-sm-12">
  <div>
      <h1>FCCT Online Transpiler</h1>
      <p>The Fedora CoreOS Config Transpiler (FCCT) translates human
         readable Fedora CoreOS Configs (FCCs) into machine readable <a href="https://github.com/coreos/ignition">Ignition</a> Configs.
         See the <a href="https://github.com/coreos/fcct/blob/master/docs/getting-started.md">getting started</a>
          guide for how to use FCCT and the <a href="https://github.com/coreos/fcct/blob/master/docs/configuration-v1_0.md">configuration spec</a>
          for everything FCCs support.
</p>
  </div>
</div>
</template>

<script>
export default {
  name: 'Introduction',
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  display: block;
  font-size: 1.5em;
  text-align: left;
  font-weight:100;
}
p {
  text-align: left;
}
#intro {
  margin-top: 2em;
  margin-bottom: 0.67em;
  position: relative;
}
</style>

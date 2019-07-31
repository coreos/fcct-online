<template>
<div class="row redhat-footer">
    <div class="container col-md-12 col-lg-12 col-sm-12">
        <a href="https://www.redhat.com" class="redhat-logo">
            <img src="../assets/Logo_RH_RGB_Reverse_Tight_Crop.svg" alt="Red Hat">
        </a>
        <p class="copyright">
            Copyright ©2019 Red Hat, Inc.</p>
    </div>
</div>
</template>

<script>
export default {
  name: 'Footer',
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.redhat-footer {
    background: #000;
    margin-top: 1em;
}
.redhat-logo {
    float: left;
    margin-left: 1em;
}
.copyright {
    color: #646464;
    display: block;
    float:right;
    margin-top: 0.2em;
    margin-bottom: 0.2em;
}
.container {
    padding: 0.5em;
}
</style>

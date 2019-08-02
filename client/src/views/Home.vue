<template>
  <div id="home">
    <Nav/>
    <MainBody/>
    <Footer/>
  </div>
</template>

<script>
// @ is an alias to /src
import Nav from '@/components/Nav.vue';
import MainBody from '@/components/MainBody.vue';
import Footer from '@/components/Footer.vue';

export default {
  name: 'home',
  components: {
    Nav,
    MainBody,
    Footer,
  },
};
</script>

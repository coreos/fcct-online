<template>
  <div class="home">
    <Nav/>
    <Content/>
    <Footer/>
  </div>
</template>

<script>
// @ is an alias to /src
import Nav from '@/components/Nav.vue';
import Content from '@/components/Content.vue';
import Footer from '@/components/Footer.vue';

export default {
  name: 'home',
  components: {
    Nav,
    Content,
    Footer,
  },
};
</script>

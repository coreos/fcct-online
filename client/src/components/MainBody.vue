<template>
  <div id="content">
    <Introduction/>
    <Validator/>
  </div>
</template>

<script>
// @ is an alias to /src
import Introduction from '@/components/Introduction.vue';
import Validator from '@/components/Validator.vue';

export default {
  name: 'main-body',
  components: {
    Introduction,
    Validator,
  },
};
</script>

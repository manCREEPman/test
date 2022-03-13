<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <input type="button" value="knopka" @click="getTestData">
    <div>{{ this.str }}</div>
    <input type="button" value="vk test" @click="getVkSecretCode">
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  data() {
    return {
      str: {
        type: String
      }
    }
  },
  components: {
    HelloWorld
  },
  methods: {
    getTestData() {
      fetch('http://91.132.102.83/test')
      .then(response => response.json())
      .then(data => this.str = data.data)
      .catch(error => console.log(error))
    },

    getVkSecretCode(){
      fetch('https://oauth.vk.com/authorize?client_id=8099115&display=popup&redirect_uri=http://91.132.102.83/test/vk_test&scope=wall&response_type=code')
      .then(response => console.log(response))
    }
  }
}
</script>

<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <input type="button" value="knopka" @click="getTestData">
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
      fetch('http://localhost:5000/test')
      .then( (response) => {
        this.str = response.json()
        console.log(this.str)
      })
      .catch(error => console.log(error))
    }
  }
}
</script>

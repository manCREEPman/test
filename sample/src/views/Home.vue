<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <input type="button" value="knopka" @click="getTestData">
    <div>{{ this.str }}</div>
    <input type="button" value="vk test" @click="getTestDbData">
    <div class="green">{{ this.db_obj.id }}</div>
    <div class="blue">{{ this.db_obj.name }}</div>
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
      },
      db_obj: {
        id: Number,
        name: String
      }
    }
  },
  components: {
    HelloWorld
  },
  methods: {
    getTestData() {
      fetch('http://91.132.102.83/api/first')
      .then(response => response.json())
      .then(data => this.str = data.data)
      .catch(error => console.log(error))
    },

    getTestDbData() {
      fetch('http://91.132.102.83/api/test_db_api')
      .then(response => response.json())
      .then(data => this.db_obj = data)
      .catch(error => this.db_obj = {id: 666, name: 'X_x'})
    }
  }
}
</script>

<style>
  .green {
    color: green;
  }

  .blue {
    color: blue;
  }
</style>
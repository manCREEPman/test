<template>
  <div>
    <Navigation :title="name"/>
    <v-btn
      @click="getTestData"
    >
      Get test data
    </v-btn>
    <div>
      {{ this.str }}
      id: {{ this.db_obj.id }}
      name: {{ this.db_obj.name }}
    </div>
  </div>
</template>

<script>
import Navigation from '@/components/Navigation.vue'
import { APIFetcher } from '@/api'

export default {
  name: 'Home',
  components: {
    Navigation
  },
  data: function() {
    return {
      str: '',
      db_obj: {
        id: 0,
        name: ''
      },
      name: 'Home'
    }
  },
  created: function() {
    APIFetcher.get('init_debug_db')
    .then(res => console.log(res))
    .catch(error => console.log(error))
  },
  methods: {
    getTestData() {
      APIFetcher.get('first')
      .then(response => response.data)
      .then(data => this.str = data.data)
      .catch(error => console.log(error))

      APIFetcher.get('test_db_api')
      .then(response => response.data)
      .then(data => this.db_obj = data)
      .catch(error => this.db_obj = {id: 666, name: 'X_x'})
    },

    getTestDbData() {
      
    }
  }
}
</script>

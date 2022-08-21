<template>
  <v-app>
   <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import { APIFetcher } from '@/api'

export default {
  name: 'App',

  data: () => ({
    //
  }),
  created() {
    
  }
};
</script>

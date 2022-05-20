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
    
    // предотвращение переходов в неавторизованной форме
    this.$router.beforeEach((to, from, next) => {
      let auth_token = document.cookie.replace(/(?:(?:^|.*;\s*)auth_token\s*\=\s*([^;]*).*$)|^.*$/, "$1")
      if(!this.$store.getters.authenticated && to.name !== 'Auth' && auth_token === ''){
        next('/auth')
      }
      else{
        next()
      }
    })

    // тут проверить куку и перенаправить на авторизацию, если её нет
    let auth_token = document.cookie.replace(/(?:(?:^|.*;\s*)auth_token\s*\=\s*([^;]*).*$)|^.*$/, "$1")
    if (auth_token === ''){
      console.log('kuk nema')
      this.$router.push('/auth')
    }
    else {
      APIFetcher.get('auth/check_auth', { withCredentials: true})
      .then(response => response.data)
      .then(
        (auth_obj) => {
          try {
            console.log('inside cookie updater')
            console.log(auth_obj)
            let loginStatus = auth_obj.auth
            if(loginStatus) {
              this.$store.dispatch('changeAuthState', loginStatus)
              console.log('inside')
              console.log(this.$store.getters.authenticated)
              this.$router.push('/')
            }
            else{
              this.$router.push('/auth')
            }
          }
          catch(e) {
            console.log(e)
          }
        }
      )
      .catch((error) => {
          console.log(error)
        }
      )
    }
  }
};
</script>

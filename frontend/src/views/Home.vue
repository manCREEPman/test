<template>
  <div>
    <Navigation title="Главная"/>
    <VkAuthBlock :authState="vkAuthState"/>
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
    <v-spacer/>
  </div>
</template>

<script>
import Navigation from '@/components/Navigation.vue'
import VkAuthBlock from '@/components/VkAuthBlock.vue'
import { APIFetcher } from '@/api'

export default {
  name: 'Home',
  components: {
    Navigation,
    VkAuthBlock
  },
  data: function() {
    return {
      str: '',
      db_obj: {
        id: 0,
        name: ''
      },
      name: 'Home',
      vkAuthState: false
    }
  },
  created: function() {
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
    console.log('auth_token: ' + auth_token)
    if (auth_token === ''){
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
            let vkLoginStatus = auth_obj.vk_auth

            if(loginStatus) {
              this.$store.dispatch('changeAuthState', loginStatus)
              if (vkLoginStatus) {
                this.$store.dispatch('changeVKAuthState', vkLoginStatus)
                console.log('inside')
                console.log(this.$store.getters.authenticated)
              }
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

    this.vkAuthState = this.$store.getters.vkAuthenticated
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

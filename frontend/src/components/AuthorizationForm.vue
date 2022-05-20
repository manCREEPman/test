<template>
    <v-card 
    class="main mx-auto mt-5"
    max-width="500px"
    :disabled="false"
    >

      <v-card-title>
        <h1 class="display-1">Авторизация</h1>
      </v-card-title>

      <v-card-subtitle style="color: red;">
        {{ authErrorMessage }}
      </v-card-subtitle>

      <v-card-text>
        <v-form>
          <v-text-field 
            label="Username"
            prepend-icon="mdi-account-circle"
            v-model="login"
          />
          <v-text-field 
            label="Password" 
            prepend-icon="mdi-lock"
            v-model="password"
            :type="showPassword ? 'text': 'password'"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
          />
        </v-form>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn 
        color="success"
        @click="registerUser"
        >
            Регистрация
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn 
        color="info"
        @click="loginUser"
        >
            Войти
        </v-btn>
      </v-card-actions>

    </v-card>
</template>

<script>
import { APIFetcher } from '@/api'

export default {
    name: 'Authorization',
    data: function () {
        return {
            showPassword: false,
            pending: false,
            login: '',
            password: '',
            authErrorMessage: ''
        }
    },
    computed: {
      pendingState() {
        return this.pending
      }
    },
    methods: {
        async registerUser() {
            if(this.login !== '' && this.password !== ''){
                // здесь заблочить форму авторизации, пока не придёт ответ (трудный момент со связкой props и реальных объектов Vue)
                this.authErrorMessage = ''

                await APIFetcher.post(
                  'auth/register', 
                  {login: this.login, password: this.password}, 
                  { withCredentials: true }
                )
                .then(response => response.data)
                .then(
                  (auth_obj) => {
                    try {
                      let registrationStatus = auth_obj.registration
                      let registrationMessage = auth_obj.message
                      if(registrationStatus) {
                        this.$store.dispatch('changeAuthState', registrationStatus)
                        this.$router.push('/')
                      }
                      else {
                        this.authErrorMessage = registrationMessage
                      }
                    }
                    catch(e) {
                      console.log(e)
                      this.authErrorMessage = 'Проблемы на стороне сервера'
                    }
                  }
                )
                .catch((error) => {
                    console.log(error)
                    this.authErrorMessage = 'Проблемы на стороне сервера'
                  }
                )
                console.log(this.$store.getters.authenticated)
                if(this.$store.getters.authenticated){
                  this.$router.push('/')
                }
            }
        },

        async loginUser() {
            if(this.login !== '' && this.password !== ''){
                // здесь заблочить форму авторизации, пока не придёт ответ (трудный момент со связкой props и реальных объектов Vue)
                this.authErrorMessage = ''

                await APIFetcher.post(
                  'auth/login', 
                  {login: this.login, password: this.password}, 
                  { withCredentials: true }
                )
                .then(response => response.data)
                .then(
                  (auth_obj) => {
                    try {
                      console.log(auth_obj)
                      let loginStatus = auth_obj.auth
                      let loginMessage = auth_obj.message
                      if(loginStatus) {
                        this.$store.dispatch('changeAuthState', loginStatus)
                        console.log('inside')
                        console.log(this.$store.getters.authenticated)
                      }
                      else {
                        this.authErrorMessage = loginMessage
                      }
                    }
                    catch(e) {
                      console.log(e)
                      this.authErrorMessage = 'Проблемы на стороне сервера'
                    }
                  }
                )
                .catch((error) => {
                    console.log(error)
                    this.authErrorMessage = 'Проблемы на стороне сервера'
                  }
                )
                console.log('outside')
                console.log(this.$store.getters.authenticated)
                if(this.$store.getters.authenticated){
                  this.$router.push('/')
                }
            }
        }
    }
}
</script>
<template>
    <v-card 
    class="mx-3 my-5"
    max-width="500px"
    :disabled="false"
    >

    <v-card-title>
        <h1 class="display-1">Статус авторизации VK</h1>
    </v-card-title>

    <v-card-subtitle :style="{ color: titleColor}">
        {{ authTitle }}
    </v-card-subtitle>
    
    <div v-if="notAuthenticated">    
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
            color="info"
            @click="loginUser"
            >
                Войти
            </v-btn>
        </v-card-actions>
    </div>

    </v-card>
</template>

<script>
import { APIFetcher } from '@/api'

export default {
    name: 'VkAuthBlock',

    data: ()=> {
        return {
            login: '',
            password: '',
            showPassword: false,
            authTitle: 'Необходима авторизация ВК',
            titleColor: 'red'
        }
    },
    
    props: {
        authState: false
    },

    computed: {
        notAuthenticated() {
            if (this.$store.getters.vkAuthenticated) {
                this.authTitle = 'Авторизация ВК успешна'
                this.titleColor = 'green'
            }
            else {
                this.authTitle = 'Необходима авторизация ВК'
                this.titleColor = 'red'
            }

            return !this.$store.getters.vkAuthenticated
        }
    },

    methods: {
        async loginUser() {
            if(this.login !== '' && this.password !== ''){
                // здесь заблочить форму авторизации, пока не придёт ответ (трудный момент со связкой props и реальных объектов Vue)
                this.authTitle = ''

                await APIFetcher.post(
                  'vk_auth/login', 
                  {vk_login: this.login, password: this.password}, 
                  { withCredentials: true }
                )
                .then(response => response.data)
                .then(
                  (auth_obj) => {
                    try {
                      console.log(auth_obj)
                      let loginMessage = auth_obj.message
                      let vkAuthState = auth_obj.vk_auth

                      if(vkAuthState) {
                        this.$store.dispatch('changeVKAuthState', vkAuthState)
                        this.titleColor = 'green'
                        this.authTitle = 'Авторизация ВК успешна'
                      }
                      else {
                        this.authTitle = loginMessage
                        this.titleColor = 'red'
                      }
                    }
                    catch(e) {
                      console.log(e)
                      this.authTitle = 'Проблемы на стороне сервера'
                      this.titleColor = 'red'
                    }
                  }
                )
                .catch((error) => {
                    console.log(error)
                    this.authTitle = 'Проблемы на стороне сервера'
                    this.titleColor = 'red'
                  }
                )
            }
        }
    }
}
</script>
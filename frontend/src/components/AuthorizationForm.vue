<template>
    <v-card class="main mx-auto mt-5">

      <v-card-title>
        <h1 class="display-1">Авторизация</h1>
      </v-card-title>

      <v-card-text>
        <v-form>
          <v-text-field 
            label="Username"
            prepend-icon="mdi-account-circle"
          />
          <v-text-field 
            label="Password" 
            :type="showPassword ? 'text': 'password'"
            prepend-icon="mdi-lock"

            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
          />
        </v-form>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn color="success">Регистрация</v-btn>
        <v-spacer></v-spacer>
        <v-btn color="info">Войти</v-btn>
      </v-card-actions>

    </v-card>
</template>

<script>
export default {
    data: () => ({
        showPassword: false
    })
}
</script>
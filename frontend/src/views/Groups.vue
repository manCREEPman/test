<template>
  <div>
    <Navigation :title="this.title"/>
    <v-list>
      
      <v-list-item to="/" class="group">
        <v-list-item-avatar>
          <v-img src="@/assets/g6avVOgpGvd9Kp3CrX4NIWEYxUpokkaxTV7LWJUql74q2dGMvos9ZD8hcJAmDoKnwqGnGtOU.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>
            Верховная Обитель Сычей
          </v-list-item-title>

          <v-list-item-subtitle>
            Аниме арты и пейзажи
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-list-item to="/" class="group">
        <v-list-item-avatar>
          <v-img src="@/assets/g6avVOgpGvd9Kp3CrX4NIWEYxUpokkaxTV7LWJUql74q2dGMvos9ZD8hcJAmDoKnwqGnGtOU.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>
            Верховная Обитель Сычей
          </v-list-item-title>

          <v-list-item-subtitle>
            Аниме арты и пейзажи
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

    </v-list>
  </div>
</template>

<script>
import Navigation from '@/components/Navigation.vue'
export default {
  components: {
    Navigation
  },
  data: function () {
    return {
      title: 'Ваши группы'
    }
  }
}
</script>

<style>
.group {
  height: 100px;
}
</style>

<template>
    <div>
        <v-app-bar
        color="deep-purple"
        dark
        >
        <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>

        <v-toolbar-title>{{ title }}</v-toolbar-title>
        </v-app-bar>

        <v-navigation-drawer
        v-model="drawer"
        absolute
        temporary
        >
        <v-list
            nav
            dense
        >
            <v-list-item-group
            active-class="deep-purple--text text--accent-4"
            >
            <v-list-item to="/">
                <v-list-item-icon>
                <v-icon>mdi-home</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Главная</v-list-item-title>
            </v-list-item>

            <v-list-item to="/groups">
                <v-list-item-icon>
                <v-icon>mdi-account-group-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Группы</v-list-item-title>
            </v-list-item>

            <v-list-item to="/auth">
                <v-list-item-icon>
                <v-icon>mdi-account-group-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Регистрация</v-list-item-title>
            </v-list-item>

            <v-list-item to="/upload">
                <v-list-item-icon>
                <v-icon>mdi-account-group-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Загрузка изображений</v-list-item-title>
            </v-list-item>

            </v-list-item-group>
        </v-list>
        </v-navigation-drawer>
    </div>
</template>

<script>
export default {
    name: 'Navigation',
    props: {
        title: ''
    },
    data: ()=> {
        return {
            drawer: Boolean
        }
    },
    created() {
        this.drawer = false
    }
}
</script>
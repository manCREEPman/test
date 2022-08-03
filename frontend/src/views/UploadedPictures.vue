<template>
    <div>
        <Navigation :title="name"/>

        <v-container
        class="justify-center"
        style="width: 1000px;">
            <v-btn
            class="mb-4">
                <v-icon>
                    mdi-folder-multiple-image
                </v-icon>
            </v-btn>

            <v-card
            outlined
            max-width="1000px"
            class="pa-4">
                <v-row
                class="img-row">
                    <v-col>
                        <div>
                            <v-img 
                            src="@/assets/1.jpg"
                            width="175px"
                            height="115px"></v-img>
                        </div>
                        <div class="category-text text-caption">
                            autumn, day, nature
                        </div>
                    </v-col>

                    <v-col>
                        <v-textarea
                        outlined
                        name="input-7-4"
                        label="Текст поста"
                        no-resize="true"
                        height="115px"
                        ></v-textarea>
                    </v-col>
                    
                    <v-col>
                        <v-text-field
                        v-model="dateFormatted"
                        label="Время публикации"
                        hint="DD.MM.YYYY HH:mm"
                        persistent-hint
                        prepend-icon="mdi-calendar-clock"
                        value="10.05.2022 11:40"
                        ></v-text-field>
                    </v-col>
                </v-row>
                
                <v-row
                class="img-row">
                    <v-col>
                        <v-img 
                        src="@/assets/2.jpg"
                        width="175px"
                        height="115px">
                        </v-img>
                        <div class="category-text text-caption">
                            spring, day, nature
                        </div>
                    </v-col>

                    <v-col>
                        <v-textarea
                        outlined
                        name="input-7-4"
                        label="Текст поста"
                        no-resize="true"
                        height="115px"
                        ></v-textarea>
                    </v-col>
                    
                    <v-col>
                        <v-text-field
                        v-model="dateFormatted"
                        label="Время публикации"
                        hint="DD.MM.YYYY HH:mm"
                        persistent-hint
                        prepend-icon="mdi-calendar-clock"
                        value="10.05.2022 11:40"
                        ></v-text-field>
                    </v-col>
                </v-row>

                <v-row
                class="img-row">
                    <v-col>
                        <v-img 
                        src="@/assets/3.jpg"
                        width="175px"
                        height="115px">
                        </v-img>
                        <div class="category-text text-caption">
                            summer, day, city
                        </div>
                    </v-col>

                    <v-col>
                        <v-textarea
                        outlined
                        name="input-7-4"
                        label="Текст поста"
                        no-resize="true"
                        height="115px"
                        ></v-textarea>
                    </v-col>
                    
                    <v-col>
                        <v-text-field
                        v-model="dateFormatted"
                        label="Время публикации"
                        hint="DD.MM.YYYY HH:mm"
                        persistent-hint
                        prepend-icon="mdi-calendar-clock"
                        value="10.05.2022 11:40"
                        ></v-text-field>
                    </v-col>
                </v-row>

                <v-row
                class="img-row">
                    <v-col>
                        <v-img 
                        src="@/assets/4.jpg"
                        width="175px"
                        height="115px">
                        </v-img>
                        <div class="category-text text-caption">
                            summer, night, nature
                        </div>
                    </v-col>

                    <v-col>
                        <v-textarea
                        outlined
                        name="input-7-4"
                        label="Текст поста"
                        no-resize="true"
                        height="115px"
                        ></v-textarea>
                    </v-col>
                    
                    <v-col>
                        <v-text-field
                        v-model="dateFormatted"
                        label="Время публикации"
                        hint="DD.MM.YYYY HH:mm"
                        persistent-hint
                        prepend-icon="mdi-calendar-clock"
                        value="10.05.2022 11:40"
                        ></v-text-field>
                    </v-col>
                </v-row>
            </v-card>

            <div
            class="d-flex flex-row-reverse">
                <v-btn
                color="primary"
                class="mt-4">
                    Опубликовать
                </v-btn>
            </div>
            
        </v-container>
    </div>
</template>

<script>
import Navigation from '@/components/Navigation.vue'

export default {
    name: 'UploadedPictures',
    components: {
        Navigation
    }, 
    data() {
        return {
            name: 'Загрузка изображений'
        }
    }
}
</script>

<style>

.image-wrapper {
    width: 175px;
    height: 115px;
}

.category-text {
    font-style: italic;
}
</style>
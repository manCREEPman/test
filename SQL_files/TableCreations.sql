/*
User - Пользователи системы
user_id – числовое (код пользователя)
login – строковое (логин пользователя vk)
password – строковое (пароль пользователя vk)
vk_user_id – строковое (id пользователя vk)
*/
CREATE TABLE USERS
(  USER_ID SERIAL PRIMARY KEY
  ,LOGIN VARCHAR(64) NOT NULL
  ,PASSWORD VARCHAR(64) NOT NULL
  ,VK_USER_ID VARCHAR(64) NOT NULL
);


/*
Group - Сообщество
group_id – числовое (код сообщества)
admin_id – числовое (администратор сообщества)
name – строковое (наименование)
vk_group_id – строковое (id сообщества vk)
*/
CREATE TABLE GROUPS
(  GROUP_ID SERIAL PRIMARY KEY
  ,ADMIN_ID INTEGER NOT NULL
  ,NAME VARCHAR(64) NOT NULL
  ,VK_GROUP_ID VARCHAR(64) NOT NULL
);

/*
User_group -Таблица для множественной связи пользователь-сообщество
user_id – числовое (код пользователя)
group_id – числовое (код сообщества)
*/
CREATE TABLE USER_GROUP
( 	 USER_ID INTEGER NOT NULL
	,GROUP_ID INTEGER NOT NULL
 
    ,FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID) ON DELETE CASCADE
    ,FOREIGN KEY (GROUP_ID) REFERENCES GROUPS(GROUP_ID) ON DELETE CASCADE

);

/*
Post -Пост в сообществе
post_id – числовое (код поста)
author_user_id – числовое (автор поста)
group_id – числовое (код сообщества)
state – числовое (состояние поста: 0 – canceled, 1 – запланировано, 2 - запощено)
created – дата (дата создания)
changed – дата (дата изменения)
changed_by - числовое (id человека, изменившего пост)
publish_date – дата (дата публикации)
text – строковое (текст поста)
*/
CREATE TABLE POST
(  POST_ID SERIAL PRIMARY KEY
  ,AUTHOR_USER_ID INTEGER NOT NULL
  ,GROUP_ID INTEGER NOT NULL
  ,STATE SMALLINT NOT NULL
  ,CREATED DATE NOT NULL
  ,CHANGED DATE
  ,CHANGED_BY INTEGER
  ,PUBLISH_DATE DATE
  ,TEXT TEXT
 
  ,FOREIGN KEY (AUTHOR_USER_ID) REFERENCES USERS(USER_ID) ON DELETE CASCADE
  ,FOREIGN KEY (GROUP_ID) REFERENCES GROUPS(GROUP_ID) ON DELETE CASCADE
);


/*
Post_attachement_image -Прикреплённое изображение поста
attachement_id – числовое (код вложения)
post_id – числовое (код поста)
image – blob (прикреплённая )
*/
CREATE TABLE POST_ATTACHEMENT_IMAGE
(  ATTACHEMENT_ID SERIAL PRIMARY KEY
  ,POST_ID INTEGER NOT NULL
  ,IMAGE BYTEA NOT NULL
 
  ,FOREIGN KEY (POST_ID) REFERENCES POST(POST_ID) ON DELETE CASCADE
);

/*
Post_attachement - Вложение поста
attachement_id – числовое (код вложения)
post_id – числовое (код поста)
vk_object – строковое (представление объекта vk или ссылка)
*/
CREATE TABLE POST_ATTACHEMENT
(  ATTACHEMENT_ID SERIAL PRIMARY KEY
  ,POST_ID INTEGER NOT NULL
  ,VK_OBJECT TEXT NOT NULL
 
  ,FOREIGN KEY (POST_ID) REFERENCES POST(POST_ID) ON DELETE CASCADE
);

/*
Uploaded_image_gtt
Временная таблица для массовой загрузки изображений для дальнейшего формирования постов
num – числовое (номер изображения)
image – blob (изображение)
*/
CREATE TEMPORARY TABLE UPLOADED_IMAGE_GTT
(  NUM SMALLINT NOT NULL
  ,IMAGE BYTEA NOT NULL
);

/*
Post_gtt - Временная таблица для хранения постов и прикреплённых к ним изображений с фиксацией порядка
id – числовое (код поста)
q_order – числовое (порядковый номер относительно других постов (для размещения))
publish_date – дата (дата публикации)
text – строковое (текст поста)
*/
CREATE TEMPORARY TABLE POST_GTT
(  ID INTEGER NOT NULL
  ,Q_ORDER INTEGER NOT NULL
  ,PUBLISH_DATE DATE
  ,TEXT TEXT 
);

/*
Post_attachement_image_gtt - id – числовой (код временного вложения)
post_gtt_id – числовой (код временного поста)
order – числовой (порядковый номер)
image – blob (изображение)
*/
CREATE TEMPORARY TABLE POST_ATTACHEMENT_IMAGE_GTT
(  POST_GTT_ID INTEGER NOT NULL
  ,Q_ORDER SMALLINT NOT NULL
  ,IMAGE BYTEA NOT NULL
);

/*
Post_attachement_gtt - Временная таблица для хранения прочих вложений для поста
id – числовой (код временного вложения)
post_gtt_id – числовой (код временного поста)
order – числовой (порядковый номер)
vk_object – строковый (представление объекта vk или ссылка)
*/
CREATE TEMPORARY TABLE POST_ATTACHEMENT_GTT
(  ID SMALLINT NOT NULL
  ,POST_GTT_ID INTEGER NOT NULL
  ,Q_ORDER SMALLINT NOT NULL
  ,VK_OBJECT TEXT NOT NULL
);

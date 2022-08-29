import numpy
import random
import json

from pprint import pprint
import traceback

VIEW_SCORE = 0.01
LIKE_SCORE = 0.1
COMMENT_SCORE = 0.5
HOUR = 3600
MINUTE = 60

OBJ = {
    'image': {
        'islands': [],
        'new_islands': [],
        'upper_name': 0 
    },
    'attachement': {
        'islands': [],
        'new_islands': [],
        'upper_name': 0 
    },
    'text': {
        'islands': [],
        'new_islands': [],
        'upper_name': 0 
    }
}

ISLAND = {
    'number': 0,
    'posts': [],
    'new_post_count': 0,
    'new_time': 0,
    'new_state': False
}

POST = {
    'rating': 0,
    'time': 0,
    'new_state': False,
    'include_image': False,
    'include_attachement': False,
    'include_text': False
}

class RecSys:

    def __init__(self) -> None:
        self.__objects = {}

    def time_to_seconds(self, time_str: str) -> int:
        time_list = time_str.split(':')
        hours = 0
        minutes = 0
        if time_list[0][0:1] == '0':
            hours = int(time_list[0][1:])
        else:
            hours = int(time_list[0])
        
        if time_list[1][0:1] == '0':
            minutes = int(time_list[1][1:])
        else:
            minutes = int(time_list[1])

        return hours * HOUR + minutes * MINUTE

    def seconds_to_time_str(self, seconds: int) -> str:
        hours = int(seconds / HOUR)
        minutes = int((seconds - hours * HOUR) / MINUTE)
        hours_str = str(hours) if hours > 10 else '0' + str(hours)
        minutes_str = str(minutes) if minutes > 10 else '0' + str(minutes)
        return f'{hours_str}:{minutes_str}'

    def create_real_post(self) -> dict:
        views = random.randint(1, 5000) 
        likes = random.randint(0, 400) 
        comments = random.randint(0, 100)
        time = random.randint(0, 86340)
        ii = random.randint(0, 1) == 1
        ia = random.randint(0, 1) == 1
        it = random.randint(0, 1) == 1

        rating = self._stats_to_number(views, likes, comments)

        if not ii and not ia and not it:
            ii = True
        
        return {
            'rating': rating,
            'time': time,
            'include_image': ii,
            'include_attachement': ia,
            'include_text': it
        }

    def _stats_to_number(self, views: int, likes: int, comments: int) -> float:
        return views * VIEW_SCORE + likes * LIKE_SCORE + comments * COMMENT_SCORE

    def create_real_posts(self, count=1000) -> list:
        real_posts = []
        for _ in range(count):
            real_posts.append(self.create_real_post())
        real_posts.sort(key= lambda x: x['rating'])
        return real_posts

    def get_calc_values_list(self, posts: list, value: str) -> list:
        posts_values = []
        for post in posts:
            posts_values.append(post[value])
        return posts_values

    def mean_of_posts(self, posts: list, value: str) -> float:
        return numpy.mean(self.get_calc_values_list(posts, value))

    def median_of_posts(self, posts: list, value: str) -> float:
        return numpy.median(self.get_calc_values_list(posts, value))

    def std_of_posts(self, posts: list, value: str) -> float:
        return numpy.std(self.get_calc_values_list(posts, value))

    def create_elements_selection(self, posts: list) -> list:
        sigma = self.std_of_posts(posts, 'rating')
        avg_rating = self.mean_of_posts(posts, 'rating')
        k1 = float(sigma / avg_rating)
        k2 = float(avg_rating / 2)

        if k1 < k2:
            base_element = avg_rating
        else:
            base_element = self.median_of_posts(posts, 'rating')

        elements_selection = [x for x in posts if x['rating'] >= base_element][:100]
        elements_selection.sort(key=lambda x: x['time'])
        return elements_selection

    def create_islands_obj(self, posts: list) -> dict:
        obj = {
            'image': {
                'islands': [],
                'new_islands': [],
                'upper_name': 0 
            },
            'attachement': {
                'islands': [],
                'new_islands': [],
                'upper_name': 0 
            },
            'text': {
                'islands': [],
                'new_islands': [],
                'upper_name': 0 
            }
        }

        def get_current_island_last_post_by_number(tag, num):
            islands = obj[tag]['islands']
            for island in islands:
                if island['number'] == num:
                    return island['posts'][len(island['posts']) - 1]


        obj_cur_islands = {
            'image': None,
            'attachement': None,
            'text': None
        }
        
        for post in posts:
            tags_needs_to_add = []
            
            if post['include_image']:
                tags_needs_to_add.append('image')
            if post['include_attachement']:
                tags_needs_to_add.append('attachement')
            if post['include_text']:
                tags_needs_to_add.append('text')

            for tag in tags_needs_to_add:
                island = {
                    'number': 0,
                    'posts': [],
                    'new_post_count': 0,
                    'new_time': 0,
                    'new_state': False
                }
                if obj_cur_islands[tag] is None:
                    island['posts'].append(post)
                    island['number'] = obj[tag]['upper_name']
                    obj[tag]['upper_name'] = obj[tag]['upper_name'] + 1
                    obj[tag]['islands'].append(island)
                    obj_cur_islands[tag] = island['number']
                else: 
                    try:
                        prev_tag_post = get_current_island_last_post_by_number(tag, obj_cur_islands[tag])
                        if abs(post['time'] - prev_tag_post['time']) > HOUR:
                            island['posts'].append(post)
                            island['number'] = obj[tag]['upper_name']
                            obj[tag]['upper_name'] = obj[tag]['upper_name'] + 1
                            obj[tag]['islands'].append(island)
                            obj_cur_islands[tag] = island['number']
                        else:
                            cur_index = 0
                            for island in obj[tag]['islands']:
                                if island['number'] == obj_cur_islands[tag]:
                                    break
                                cur_index = cur_index + 1
                            obj[tag]['islands'][cur_index]['posts'].append(post)
                    except:
                        print(traceback.format_exc())
                        pprint(obj_cur_islands)
                        pprint(tag)
                        print()
        return obj                        

    def make_choise(self, percent: int) -> bool:
        value = random.randint(1, 100)
        return 1 <= value <= percent
        
    def sort_islands_by_rating(self, obj: dict):
        for tag in obj.keys():
            islands_count = len(obj[tag]['islands'])
            for i in range(islands_count):
                avg_island_rating = self.mean_of_posts(obj[tag]['islands'][i]['posts'], 'rating')
                obj[tag]['islands'][i].setdefault('avg_rating', avg_island_rating)
        
            obj[tag]['islands'].sort(key=lambda x: x['avg_rating'])
    
    def get_posts_density(self, posts: list) -> float:
        if len(posts) == 0:
            return 0
        else:
            k = 0
            for i in range(len(posts) - 1):
                if abs(posts[i]['time'] - posts[i + 1]['time']) > 10 * MINUTE:
                    k = k + 1
            return float(k / len(posts))

    def get_correct_time_addition(self, time1: int, time2: int, sign: int = 1) -> int:
        if sign > 0:
            if time1 + time2 > 24 * HOUR - MINUTE:
                return time1 + time2 - (24 * HOUR - MINUTE)
            else:
                return time1 + time2
        else:
            if time1 - time2 < 0:
                return time2 - time1
            else:
                return time1 - time2

    def make_recommendation(self, vk_login: str, post_type: str):
        PERCENT = 70
        CHANSE_OF_BORDER_TIME = 50
        DENSITY_BORDER = 0.5
        NEW_POSTS_COUNT_TO_UNION = 10

        obj = self.__objects.get(vk_login)
        if obj:
            to_new = False
            index = 0

            new_islands_count = len(obj[post_type]['new_islands'])
            islands_count = len(obj[post_type]['islands'])
            if new_islands_count > 0:
                to_new = True
                # выбираем новый остров
                if self.make_choise(PERCENT):
                    index = 0
                else:
                    index = len(obj[post_type]['new_islands']) - 1
            
            if islands_count > 1 and not to_new:
                if self.make_choise(PERCENT):
                    index = len(obj[post_type]['islands']) - 1
                else:
                    index = len(obj[post_type]['islands']) - 2
            elif islands_count <= 1 and not to_new:
                if islands_count == 1:
                    island = {
                        'number': obj[post_type]['upper_name'],
                        'posts': [],
                        'new_post_count': 0,
                        'new_time': self.get_correct_time_addition(max_t, s * HOUR),
                        'new_state': True
                    }
                    obj[post_type]['upper_name'] = obj[post_type]['upper_name'] + 1
                    obj[post_type]['new_islands'].append(island)

                    island = {
                        'number': obj[post_type]['upper_name'],
                        'posts': [],
                        'new_post_count': 0,
                        'new_time': self.get_correct_time_addition(min_t, s * HOUR, -1),
                        'new_state': True
                    }
                    obj[post_type]['upper_name'] = obj[post_type]['upper_name'] + 1
                    obj[post_type]['new_islands'].append(island)


                    # ===================================================================
            

                    island_base_time = obj[post_type]['new_islands'][0]['new_time']
                    if self.make_choise(CHANSE_OF_BORDER_TIME):
                        min_t = self.get_correct_time_addition(island_base_time, 5 * MINUTE, -1)
                        max_t = island_base_time
                    else:
                        min_t = island_base_time
                        max_t = self.get_correct_time_addition(island_base_time, 5 * MINUTE)

                    new_time = random.randint(min_t, max_t)
                    new_post = self.create_real_post()
                    new_post['time'] = new_time
                    new_post.setdefault('new_state', True)
                    obj[post_type]['new_islands'][0]['posts'].append(new_post)
                    obj[post_type]['new_islands'][0]['new_posts'] = obj[post_type]['new_islands'][0]['new_posts'] + 1


            islands_count = len(obj[post_type]['islands'])

            if islands_count > 1:

                top1_island_posts = None
                substraction_index = 0
                if self.make_choise(PERCENT):
                    substraction_index = 1
                else:
                    substraction_index = 2

                top1_island_posts = obj[post_type]['islands'][islands_count - substraction_index]['posts']

                density = self.get_posts_density(top1_island_posts)
                    
                min_t = top1_island_posts[0]['time']
                max_t = top1_island_posts[len(top1_island_posts) - 1]['time']
                if density < DENSITY_BORDER:
                    if self.make_choise(CHANSE_OF_BORDER_TIME):
                        max_t = min_t
                        min_t = self.get_correct_time_addition(min_t, 5 * MINUTE, -1)
                    else:
                        min_t = max_t
                        max_t = self.get_correct_time_addition(max_t, 5 * MINUTE)
                
                new_time = random.randint(min_t, max_t)
                new_post = self.create_real_post()
                new_post['time'] = new_time
                new_post.setdefault('new_state', True)

                obj[post_type]['islands'][islands_count - substraction_index]['posts'].append(new_post)
                obj[post_type]['islands'][islands_count - substraction_index]['new_posts_count'] = obj[post_type]['islands'][islands_count - substraction_index]['new_posts_count'] + 1

                if obj[post_type]['islands'][islands_count - 1]['new_posts_count'] >= NEW_POSTS_COUNT_TO_UNION:
                    pass

                obj[post_type]['islands'][islands_count - 1]['posts'].sort(key=lambda x: x['time'])


            elif islands_count == 1:
                if len(obj[post_type]['new_islands']) == 0:
                    s = random.randint(1, 5)

                    cur_island_posts = obj[post_type]['islands'][0]['posts']
                    max_t = cur_island_posts[len(cur_island_posts) - 1]['time']
                    min_t = cur_island_posts[0]['time']
                
                    island = {
                        'number': obj[post_type]['upper_name'],
                        'posts': [],
                        'new_post_count': 0,
                        'new_time': self.get_correct_time_addition(max_t, s * HOUR),
                        'new_state': True
                    }
                    obj[post_type]['upper_name'] = obj[post_type]['upper_name'] + 1
                    obj[post_type]['new_islands'].append(island)

                    island = {
                        'number': obj[post_type]['upper_name'],
                        'posts': [],
                        'new_post_count': 0,
                        'new_time': self.get_correct_time_addition(min_t, s * HOUR, -1),
                        'new_state': True
                    }
                    obj[post_type]['upper_name'] = obj[post_type]['upper_name'] + 1
                    obj[post_type]['new_islands'].append(island)
                
                min_t = 0
                max_t = 0
                if self.make_choise(PERCENT):
                    island_base_time = obj[post_type]['new_islands'][0]['new_time']
                    if self.make_choise(CHANSE_OF_BORDER_TIME):
                        min_t = self.get_correct_time_addition(island_base_time, 5 * MINUTE, -1)
                        max_t = island_base_time
                    else:
                        min_t = island_base_time
                        max_t = self.get_correct_time_addition(island_base_time, 5 * MINUTE)

                    new_time = random.randint(min_t, max_t)
                    new_post = self.create_real_post()
                    new_post['time'] = new_time
                    new_post.setdefault('new_state', True)
                    obj[post_type]['new_islands'][0]['posts'].append(new_post)
                    obj[post_type]['new_islands'][0]['new_posts'] = obj[post_type]['new_islands'][0]['new_posts'] + 1
                else:
                    top1_island_posts = obj[post_type]['islands'][0]['posts']
                    density = self.get_posts_density(top1_island_posts)
                    
                    min_t = top1_island_posts[0]['time']
                    max_t = top1_island_posts[len(top1_island_posts) - 1]['time']
                    if density < DENSITY_BORDER:
                        if self.make_choise(CHANSE_OF_BORDER_TIME):
                            max_t = min_t
                            min_t = self.get_correct_time_addition(min_t, 5 * MINUTE, -1)
                        else:
                            min_t = max_t
                            max_t = self.get_correct_time_addition(max_t, 5 * MINUTE)

                    new_time = random.randint(min_t, max_t)
                    new_post = self.create_real_post()
                    new_post['time'] = new_time
                    new_post.setdefault('new_state', True)
                    obj[post_type]['islands'][0]['new_posts'] = obj[post_type]['islands'][0]['new_posts'] + 1
            else:
                pass

    def init_example_posts(self):
        pass

s = RecSys()
# posts = s.create_real_posts(count=20)
# selected_posts = s.create_elements_selection(posts)
# pprint(s.create_islands_obj(selected_posts))
import scrapy
import re
import json
from scrapy.http import HtmlResponse
from Instagram.items import InstagramItem
import hashlib


class InstagramSpider(scrapy.Spider):
    """
    Класс паука для парсинга 'Instagram.com'
    """
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = '' # логин
    insta_pass = '' # хешпароль
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/' # ссылка на страницу авторизации
    graphql_url = 'https://i.instagram.com/api/v1/friendships/' # ссылка на запрос списка друзей
    users = ['yoshkinkrot', 'montanakauai', 'pipykins'] # список друзей

    def parse(self, response: HtmlResponse):
        """
        Метод открывающий страницу авторизации
        """
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf}
                                 )

    def user_login(self, response: HtmlResponse):
        """
        Метод запроса на авторизацию
        """
        j_body = response.json()
        if j_body['authenticated']:
            for user in self.users:
                yield response.follow(f'/{user}/',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': user})

    def user_data_parse(self, response: HtmlResponse, username):
        """
        Метод запроса на всех подписчиков и подписок
        """
        user_id = self.fetch_user_id(response.text, username)

        url_following = f'{self.graphql_url}{user_id}/following/?count=12'
        yield response.follow(url_following,
                              callback=self.follow_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'fol_list': 'following'},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        url_followers = f'{self.graphql_url}{user_id}/followers/?count=12'
        yield response.follow(url_followers,
                              callback=self.follow_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'fol_list': 'followers'},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def follow_parse(self, response: HtmlResponse, username, user_id, fol_list):
        """
        Метод парсинга подписчиков и подписок, и формирования Item
        """
        j_data = response.json()
        if j_data['next_max_id']:
            # запрос на следующие 12 подписчиков или подписок
            max_id = j_data['next_max_id']
            url_following = f'{self.graphql_url}{user_id}/{fol_list}/?count=12&max_id={max_id}'
            yield response.follow(  url_following,
                                    callback=self.follow_parse,
                                    cb_kwargs={ 'username': username,
                                                'user_id': user_id,
                                                'fol_list': fol_list},
                                    headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        for user in j_data['users']:
            # формирование Item по полученным данным
            yield InstagramItem(_id=hashlib.sha1(str(user).encode()).hexdigest(),
                                follow_list=fol_list,
                                fol_username=user['username'],
                                fol_user_id=user['pk'],
                                pic_url=user['profile_pic_url'],
                                j_body=user,
                                username=username,
                                user_id=user_id
                                )

    def fetch_csrf_token(self, text: str) -> str:
        """
        Получаем токен для авторизации
        :param text:
        :return:
        """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        """
        Получаем id желаемого пользователя
        :param text:
        :param username:
        :return:
        """
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')

from django.test import TestCase
from django.test import Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

class TestView(TestCase):

    def setUp(self):
        self.client=Client()
        self.user_trump=User.objects.create_user(username='trump',password='somepassword')
        self.user_obama=User.objects.create_user(username='obama',password="somepassword")

        self.category_programming=Category.objects.create(name="programming",slug="programming")
        self.category_music=Category.objects.create(name="music",slug="music")

        self.post_001 = Post.objects.create(
            title="첫번째 포스트 입니다.",
            content="Hello World. We are the world",
            author=self.user_trump,
            category=self.category_programming,
        )
        self.post_002 = Post.objects.create(
            title="두 번째 포스트 입니다.",
            content="1등이 전부는 아니 잖아요?",
            author=self.user_obama,
            category=self.category_music,
        )
        self.post_003 = Post.objects.create(
            title="세 번째 포스트 입니다.",
            content="카테고리가 없을 수도 있죠",
            author=self.user_obama,
        )

    def category_card_test(self,soup):
        categories_card=soup.find('div', id='categories-card')
        self.assertIn('Categories',categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})',categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_programming.post_set.count()})',categories_card.text)
        self.assertIn(f'미분류 ({Post.objects.filter(category=None).count()})',categories_card.text)



    def navar_test(self,soup):
        navbar = soup.nav
        self.assertIn("Blog", navbar.text)
        self.assertIn("About me", navbar.text)

        log_btn=navbar.find('a',text="MINI_0u0")
        self.assertEqual(log_btn.attrs['href'] , '/')

        home_btn=navbar.find('a',text='Home')
        self.assertEqual(home_btn.attrs['href'] , '/')

        blog_btn=navbar.find('a',text='Blog')
        self.assertEqual(blog_btn.attrs['href'] , '/blog/')

        about_me_btn=navbar.find('a',text='About me')
        self.assertEqual(about_me_btn.attrs['href'] , '/about_me/')


    
    def test_post_list(self):

        #포스트가 3개있는지 확인
        self.assertEqual(Post.objects.count(),3)
        #두개의 정보가 동일한지 확인
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content,'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        self.navar_test(soup)
        self.category_card_test(soup)



        self.assertEqual(Post.objects.count(),3)
        main_area=soup.find('div',id='main-area')
        self.assertNotIn("아직 게시물이 없습니다.",main_area.text)

        post_001_card=main_area.find('div',id="post-1")
        self.assertIn(self.post_001.title,post_001_card.text)
        self.assertIn(self.post_001.category.name,post_001_card.text)

        post_002_card = main_area.find('div', id="post-2")
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id="post-3")
        self.assertIn("미분류", post_001_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(),main_area.text)
        self.assertIn(self.user_obama.username.upper(),main_area.text)

        Post.objects.all().delete()

        self.assertEqual(Post.objects.count(),0)
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content,'html.parser')

        main_area=soup.find('div',id = 'main-area')
        self.assertIn("아직 게시물이 없습니다.",main_area.text)

        # self.assertIn(post_001.title, main_area.text)
        # self.assertIn(post_002.title, main_area.text)







        

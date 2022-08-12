from django.test import TestCase
from django.test import Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):

    def setUp(self):
        self.client=Client()
    
    def test_post_list(self):
        #두개의 정보가 동일한지 확인
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content,'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        navbar=soup.nav
        self.assertIn('Blog',navbar.text)
        self.assertIn('About me',navbar.text)

        self.assertEqual(Post.objects.count(),0)
        main_area=soup.find('div',id='main-area')
        self.assertIn("아직 게시물이 없습니다.",main_area.text)

        post_001=Post.objects.create(
            title="첫번째 포스트 입니다.",
            content="Hello World. We are the world",
        )
        post_002=Post.objects.create(
            title="두 번째 포스트 입니다.",
            content="1등이 전부는 아니 잖아요?",
        )
        self.assertEqual(Post.objects.count(),2)

        response=self.client.get('/blog/')
        soup=BeautifulSoup(response.content,'html.parser')
        self.assertEqual(response.status_code,200)
        main_area=soup.find('div',id = 'main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn("아직 게시물이 없습니다.",main_area.text)

    def test_post_detail(self):
        post_001=Post.objects.create(
            title="첫 번째 포스트 입니다.",
            content="Hello World. We are the world",
        )

        self.assertEqual(post_001.get_absolute_url(), '/blog/1/') #'/blog/1'

        response=self.client.get(post_001.get_absolute_url())#접속을 할 때는 /하나를 더 추가 해주어야 함 #'/blog/1/'   post_001.get_absolute_url()
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content,'html.parser')

        navbar=soup.nav
        self.assertIn("Blog", navbar.text)
        self.assertIn("About me", navbar.text)

        self.assertIn(post_001.title , soup.title.text)

        main_area=soup.find('div', id="main-area")
        post_area=main_area.find('div', id="post-area")
        self.assertIn(post_001.title,post_area.text)

        self.assertIn(post_001.content , post_area.text)


        

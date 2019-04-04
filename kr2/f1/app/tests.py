import re

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from .models import Student, Teacher, Mark


# Create your tests here.
class PagesTests(TestCase):
    fixtures = [
        'testing.json'
    ]

    def test_index(self):
        resp = self.client.get(reverse('index'))

        self.assertEqual(resp.status_code, 200)

    def test_redirect(self):
        Mark.objects.create(
            subject='Test1',
            mark=7,
            student=Student.objects.first(),
            teacher=Teacher.objects.last()
        )
        Mark.objects.create(
            subject='Test2',
            mark=4,
            student=Student.objects.last(),
            teacher=Teacher.objects.first()
        )
        Mark.objects.create(
            subject='Test3',
            mark=1,
            student=Student.objects.last(),
            teacher=Teacher.objects.last()
        )

        resp = self.client.get(reverse('index'))

        self.assertRedirects(
            resp,
            expected_url=reverse('info'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )


class SeleniumMarksTests(StaticLiveServerTestCase):
    fixtures = [
        'testing.json'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(executable_path=r'D:\Work\Geckodriver\geckodriver.exe')
        cls.selenium.implicitly_wait(10)

    def test_create_mark(self):
        self.selenium.get(f'{self.live_server_url}/mark/student/1')
        subject_input = self.selenium.find_element_by_name('subject')
        subject_input.send_keys('Selenium Mark')
        mark_input = self.selenium.find_element_by_name('mark')
        mark_input.send_keys('4')
        teacher = Select(self.selenium.find_element_by_name('teacher'))
        teacher.select_by_value('1')
        self.selenium.find_element_by_xpath('//input[@value="Save"]').click()

        self.selenium.get(f'{self.live_server_url}/student/1')
        source = self.selenium.page_source
        self.assertNotEqual(re.search('Selenium Mark', source), None)

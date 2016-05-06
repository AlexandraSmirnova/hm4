# -*- coding: utf-8 -*-
import os
import unittest

from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver import DesiredCapabilities, Remote

from tests.pages import PageOffer


class SliderTestCase(unittest.TestCase):
    OFFER_NUM = 2

    def setUp(self):
        self.browser = os.environ.get('HW4BROWSER', 'CHROME')
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, self.browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def testSlider(self):
        offer_page = PageOffer(self.driver)
        offer_page.open(self.OFFER_NUM)
        slider = offer_page.slider
        slider.open_slider()

        slider.click_next()
        slider.click_next(1)
        slider.click_prev()
        slider.click_prev(1)
        
        #self.assertEqual(slider.get_page_num(), slider.get_page_num_from_browser())
        # проверяем наличие всех кнопок для соц.сетей
        # chare_block = slider.chare_block
        # chare_block.click_all_btn()
        # banner = slider.banner
        # banner.find()

        # проверка, что у первого элемента нет перехода назад
        with self.assertRaises(ElementNotVisibleException):
            slider.click_prev()

        slider.close_slider(1)
        slider.open()
        # проверка, что у последнего элемента нет перехода вперед
        all_photos_num = slider.get_max_page_num()
        for i in range(1, all_photos_num):
             slider.click_next()
        with self.assertRaises(ElementNotVisibleException):
             slider.click_next()


        # проверяем, что можно перейти на интересующий слайд с помощью картинок-превью
        slider.go_to_slide(0)
        self.assertEqual(slider.get_page_num_from_browser(), 1)
        #slider.click_next(2)


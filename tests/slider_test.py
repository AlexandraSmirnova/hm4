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

    def testSliderPrevNext(self):
        slider = self.getSlider()
        slider.open_slider()

        # обычный переход по стрелкам
        slider.click_next()
        slider.click_prev()
        # переход по краям страницы
        slider.click_next(1)
        slider.click_prev(1)

        # проверка, что у первого элемента нет перехода назад
        with self.assertRaises(ElementNotVisibleException):
            slider.click_prev()

        # проверка, что у последнего элемента нет перехода вперед
        all_photos_num = slider.get_max_page_num()
        for i in range(1, all_photos_num):
            slider.click_next()
        with self.assertRaises(ElementNotVisibleException):
            slider.click_next()

    def testSliderNum(self):
        slider = self.getSlider()
        slider.open_slider()

        self.assertEqual(slider.get_page_num(), slider.get_page_num_from_browser())
        all_photos_num = slider.get_max_page_num()
        slider.go_to_slide(all_photos_num - 1)
        self.assertEqual(slider.get_page_num(), slider.get_page_num_from_browser())

    def testSliderClose(self):
        slider = self.getSlider()
        slider.open_slider()

        # закрытие по кнопке в левом верхнем углу
        slider.close_slider()
        with self.assertRaises(ElementNotVisibleException):
            slider.go_to_slide(0)

        # проверка закрытия слайдера при нажати на затемненную площадь вокруг фото
        slider.open_slider()
        slider.close_slider(1)
        with self.assertRaises(ElementNotVisibleException):
            slider.go_to_slide(0)

    def testSliderPreview(self):
        slider = self.getSlider()
        slider.open_slider()

        # проверяем, что можно перейти на интересующий слайд с помощью картинок-превью
        slider.go_to_slide(0)
        self.assertEqual(slider.get_page_num_from_browser(), 1)
        all_photos_num = slider.get_max_page_num()
        slider.go_to_slide(all_photos_num - 1)
        self.assertEqual(slider.get_page_num(), slider.get_page_num_from_browser())

    def testSliderShare(self):
        slider = self.getSlider()
        slider.open_slider()

        # проверяем наличие всех кнопок для соц.сетей
        chare_block = slider.chare_block
        chare_block.click_all_btn()
        banner = slider.banner
        banner.find()

    def getSlider(self):
        offer_page = PageOffer(self.driver)
        offer_page.open(self.OFFER_NUM)
        return offer_page.slider

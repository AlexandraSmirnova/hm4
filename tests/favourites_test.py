# -*- coding: utf-8 -*-
import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote

from tests.pages import AuthPage, PageOffer, FavouritesPage, FavouriteItem


class FavouritesTestCase(unittest.TestCase):
    USEREMAIL = 'smirnova-a-yu'
    USERPASSWORD = os.environ.get('HW4PASSWORD')
    OFFER_NUM = 2

    def setUp(self):
        self.browser = os.environ.get('HW4BROWSER', 'CHROME')
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, self.browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.USEREMAIL)
        auth_form.set_password(self.USERPASSWORD)
        auth_form.submit()

        # основная проверка добавления в избранное
        offer_page = PageOffer(self.driver)
        favorites_page = FavouritesPage(self.driver)
        offer_page.open(self.OFFER_NUM)
        offer_page.add_to_favourites()
        favorites_page.open()
        new_count = favorites_page.get_count()
        self.assertEqual(new_count, 1)

        # проверка нахождения в избранном добавленного объявления
        f_item = FavouriteItem(self.driver)
        f_item.open()
        check_page = PageOffer(self.driver)
        check_page.set_offer_id()
        self.assertEqual(offer_page.get_offer_id(), check_page.get_offer_id())

        # проверяем, что при повторном нажатии на кнопку "в избранное", элемент удалится
        check_page.add_to_favourites()
        favorites_page.open()
        new_count = favorites_page.get_count()
        self.assertEqual(new_count, 0)

        # проверка удаления избранного из страницы избранное
        offer_page.open(self.OFFER_NUM)
        offer_page.add_to_favourites()
        favorites_page.open()
        favorites_page.clear_list()
        favorites_page.open()   # обновим страницу
        count = favorites_page.get_count()
        self.assertEqual(count, 0)

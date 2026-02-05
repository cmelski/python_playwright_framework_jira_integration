from page_objects.inventory_page import InventoryPage
from page_objects.login_page import LoginPage
from core.logging_utils import logger_utility

import pytest
import allure
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.login_kwargs
#@pytest.mark.xfail(reason="SCRUM-13: login broken")
def test_login_kwargs(page):
    login = LoginPage(page)
    try:
        expect(page.locator(login.login_button)).to_be_visible()
        logger_utility().info('Login page loaded')
    except AssertionError:
        logger_utility().error('Login button not visible. Test failed')
        raise
    login.click_login(username='standard_user', password='secret_sauce')
    inventory_page = InventoryPage(page)
    inventory_page_title = inventory_page.get_page_title()
    try:
        assert 'Inventory' in inventory_page_title, 'Assertion error: "Products" not in inventory page title'
        logger_utility().info('"Products" text found in inventory page title. Test passed.')
    except AssertionError:
        logger_utility().error('Assertion error: "Products" not in inventory page title. Test failed.')
        raise


@pytest.mark.regression
@pytest.mark.login_args
def test_login_args(page):

    login = LoginPage(page)
    try:
        expect(page.locator(login.login_button)).to_be_visible()
        logger_utility().info('Login page loaded')
    except AssertionError:
        logger_utility().error('Login button not visible. Test failed')
        raise

    login.click_login('standard_user', 'secret_sauce')
    inventory_page = InventoryPage(page)
    inventory_page_title = inventory_page.get_page_title()
    try:
        assert 'Inventory' in inventory_page_title, 'Assertion error: "Products" not in inventory page title'
        logger_utility().info('"Products" text found in inventory page title. Test passed')
    except AssertionError:
        logger_utility().error('Assertion error: "Products" not in inventory page title')
        raise


@pytest.mark.parametrize('invalid_login_credentials',
                         [pytest.param(('Bad username/Correct password', 'bad_username', 'secret_sauce')),
                          pytest.param(('Correct username/Bad password', 'standard_user', 'bad_password')),
                          pytest.param(('Empty username and password', '', ''))
                          ])
@pytest.mark.invalid_login
def test_invalid_login(page, invalid_login_credentials):
    login = LoginPage(page)
    try:
        expect(page.locator(login.login_button)).to_be_visible()
        logger_utility().info('Login page loaded')
    except AssertionError:
        logger_utility().error('Login button not visible. Test failed')
        raise
    scenario = invalid_login_credentials[0]
    username = invalid_login_credentials[1]
    password = invalid_login_credentials[2]
    login.click_login(username, password)
    try:
        expect(page.locator('[data-test="error"]')).to_be_visible()
        logger_utility().info(f'Error message shown. Login failed for {scenario} scenario.'
                              f' "{username}"/"{password}". Test passed')
    except AssertionError:
        logger_utility().error('Assertion error: Error message not shown. Test failed')
        raise


@pytest.mark.skip(reason="Feature not implemented yet")
@pytest.mark.smoke
def test_checkout():
    pass


@pytest.mark.xfail(reason="BUG-123: View Product broken")
@pytest.mark.regression
def test_view_product():
    assert False

@pytest.mark.dummy
def test_allure_dummy():
    allure.attach("Hello Allure", name="dummy_text", attachment_type=allure.attachment_type.TEXT)
    assert False  # force failure

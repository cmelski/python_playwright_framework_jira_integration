from page_objects.base_page import BasePage


class LoginPage():
    def __init__(self, page):
        self.page = page
        self.base_actions = BasePage(page)
        self.username_input = '#user-name'
        self.password_input = '#password'
        self.login_button = "#login-button"

    def click_login(self, *args, **kwargs):

        if args:
            username = args[0]
            password = args[1]
        else:
            username = kwargs.get('username')
            password = kwargs.get('password')

        self.base_actions.fill_fields(
            [self.username_input, self.password_input],
            [username, password]
        )

        self.base_actions.click(self.login_button)

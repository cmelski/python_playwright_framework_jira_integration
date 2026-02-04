from core.logging_utils import logger_utility

class BasePage:
    def __init__(self, page):
        self.page = page

    def click(self, selector):
        self.page.locator(selector).click()
        logger_utility().info(f'{selector} clicked')

    def fill(self, selector, value):
        self.page.locator(selector).fill(value)

    def fill_fields(self, selectors, values):
        for index, (selector, value) in enumerate(zip(selectors, values), start=1):
            logger_utility().info(f"Step {index}: Filling {selector}")
            self.page.fill(selector, value)


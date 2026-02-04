from page_objects.base_page import BasePage


class InventoryPage(BasePage):

    def get_page_title(self):

        return self.page.locator(".title").inner_text()

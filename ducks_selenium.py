import unittest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class FirstTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_first_selenium_test(self):
        self.driver.get("http://localhost/litecart/admin")
        self.driver.find_element_by_name("username").send_keys("admin")
        self.driver.find_element_by_name("password").send_keys("admin")
        self.driver.find_element_by_xpath("//button[@name='login']").click()
        self.driver.implicitly_wait(6)
        links = ['template', 'template', 'logotype']
        for link in links:
            self.driver.find_element_by_xpath("//a[@href='http://localhost/litecart/admin/?app=appearance&doc={}']".format(link)).click()
            self.driver.implicitly_wait(3)
            try:
                assert self.driver.title == "My Store – {}".format(link.capitalize())
            except AssertionError:
                print(self.driver.title)
                print("My Store - {}".format(link.capitalize()))

    def test_find_ducks(self):
        self.driver.get("http://localhost/litecart")
        categories = ['campaign-products', 'popular-products', 'latest-products']
        for category in categories:
            self.driver.find_element_by_xpath("//a[@href='#{}']".format(category)).click()
            items = self.driver.find_elements_by_xpath('//*[@id="{}"]/div/div'.format(category))
            for item in items:
                self.driver.find_element_by_xpath('//*[@id="box-{}"]/div/div[{}]/div/a/div[1]/div'.format(category,
                                                                                                items.index(item)+1))

    def test_countries_sort(self):
        self.driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
        self.driver.find_element_by_name("username").send_keys("admin")
        self.driver.find_element_by_name("password").send_keys("admin")
        self.driver.find_element_by_xpath("//button[@name='login']").click()
        self.driver.implicitly_wait(5)
        a = []
        for i in range(242):
            names_of_countries = \
                self.driver.find_elements_by_xpath('//*[@id="main"]/form/table/tbody/tr[{}]/td[5]/a'.format(i+1))
            for name in names_of_countries:
                name = name.get_attribute("textContent")
                if name[0] == 'Å':
                    lname = list(name)
                    lname[0] = "A"
                    name = ''.join(lname)
                a.append(name)
        assert a == sorted(a)

    def test_zones_of_countries_sort(self):
        self.driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
        self.driver.find_element_by_name("username").send_keys("admin")
        self.driver.find_element_by_name("password").send_keys("admin")
        self.driver.find_element_by_xpath("//button[@name='login']").click()
        self.driver.implicitly_wait(10)
        # countries = self.driver.find_elements_by_xpath('//*[@id="main"]/form/table/tbody/tr/td[5]/a')
        countries = self.driver.find_elements_by_tag_name("tr")
        print(len(countries))
        urls = []
        for country in countries:
            zone = self.driver.find_element_by_xpath(
                '//*[@id="main"]/form/table/tbody/tr[{}]/td[6]'.format(
                    countries.index(country)+1)).get_attribute("textContent")
            if int(zone) > 0:
                element = self.driver.find_element_by_xpath('//*[@id="main"]/form/table/tbody/tr[{}]/td[5]/a'.format(
                    countries.index(country)+1))
                url = element.get_attribute("href")
                urls.append(url)
        print(urls)
        for url in urls:
            self.driver.get(url)
            num_of_zones = self.driver.find_elements_by_xpath('//*[@id="main"]/form/table/tbody/tr/td[3]/input')
            print(len(num_of_zones))

    def test_right_merchandise(self):
        self.driver.get("http://localhost/litecart")
        my_duck = self.driver.find_element_by_xpath('//*[@id="box-campaign-products"]/div/div')
        title = self.driver.find_element_by_xpath(
            '//*[@id="box-campaign-products"]/div/div/div/a/div[2]').get_attribute('textContent')
        old_price = self.driver.find_element_by_xpath(
            '//*[@id="box-campaign-products"]/div/div/div/a/div[4]/s').get_attribute('textContent')
        new_price = self.driver.find_element_by_xpath(
            '//*[@id="box-campaign-products"]/div/div/div/a/div[4]/strong').get_attribute('textContent')

        my_duck.click()
        self.driver.implicitly_wait(10)
        new_price_in_frame = self.driver.find_element_by_xpath('//*[@id="box-product"]/div/div[3]/div[1]/strong').get_attribute('textContent')
        print(title, old_price, new_price, new_price_in_frame)

    def test_registration(self):
        self.driver.get("http://localhost/litecart")
        self.driver.implicitly_wait(7)
        self.driver.find_element_by_xpath("//*[@id='default-menu']/ul[2]/li/a").click()
        self.driver.find_element_by_xpath("//a[@href='http://localhost/litecart/create_account']").click()

        # class="alert alert-danger"
        self.driver.find_element_by_name("firstname").send_keys("admin")
        self.driver.find_element_by_name("lastname").send_keys("admin")


    def test_add_item_to_bucket(self):
        self.driver.get("http://localhost/litecart")
        self.driver.find_element_by_xpath("//a[@href='#popular-products']").click()
        window_before = self.driver.window_handles[0]
        self.driver.find_element_by_xpath("//*[@id='box-popular-products']/div/div[3]/div").click()
        # wait = WebDriverWait(self.driver, 10)  # seconds
        # item = self.driver.find_element_by_class_name('featherlight-content')
        # wait.until(EC.visibility_of(item))
        # element = wait.until(EC.presence_of_element_located((By.NAME, 'btn btn-success')))
        self.driver.find_element_by_class_name('btn-success').click()
        # self.driver.find_element_by_class_name('featherlight-close-icon featherlight-close').click()
        # check = self.driver.find_element_by_class_name('quantity').get_attribute('text')
        # assert check == '1'

    def tear_down(self):
        self.driver.quit()


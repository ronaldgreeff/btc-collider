import os
import csv
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Driver_Config():
    """ For Driver cconsistency, set things like
    headless state, browser driver and window size """

    options = Options()
    options.headless=True
    driver = webdriver.Firefox(options=options)
    # driver.set_window_size(4000, 1600)
    # driver.maximize_window()

class Driver(Driver_Config):
    """ Main driver for navigating to webpage and interacting with it """

    def __init__(self, script):
        self.driver = Driver_Config.driver
        self.script = open(script).read()

    def quit(self, m=None):
        """ Quit the driver """
        print('{}\n...quitting'.format(m))
        self.driver.quit()

    def process_page(self, url):
        """ """
        try:
            try:
                self.driver.get(url)
            except Exception as e:
                self.quit(m='failed to get url: {}'.format(e))

            extract = self.driver.execute_script(self.script)
            return extract # .encode('utf-8')

        except Exception as e:
            self.quit(m='failed to process_page: {}'.format(e))

if __name__ == '__main__':

    script = os.path.join(os.path.dirname(__file__), 'inject.js')
    slnm_driver = Driver(script)

    for i in range(1, 101):
        url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-{}.html'.format(i)
        extract = slnm_driver.process_page(url)
        if extract:
            for c, e in enumerate(extract):
                print(c, e)
            # with open('data.csv', 'w', newline='') as csvfile:
            #     data_w = csv.writer(csvfile, delimiter=' ',
            #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #     for e in extract:
            #         data_w.writerow(e)
        break
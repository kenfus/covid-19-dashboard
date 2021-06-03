from seleniumbase import BaseCase
import cv2
import time

##PARAMS FOR TESTS
url = "http://localhost:8501"


class Global_View(BaseCase):
    def test_basics(self):
        self.open(url)
        self.assert_no_404_errors() 
        self.assert_title("main · Streamlit")
        self.assert_text("Our World in Data")
        self.assert_text("Albania: Total cases.", timeout=30)
        self.assert_text("New data fetched from https://github.com/owid!")
        self.click("div.block-container:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > svg:nth-child(1)")
        self.click_xpath("/html/body/div[1]/div[2]/div/div/div[3]/div/div/div/ul/div/div/li[7]/span")
        self.assert_text("Global View: Total cases per million", timeout=30)
        self.assert_element_present(".stPlotlyChart")

class InternetAccess(BaseCase):
    def test_basics(self):
        self.open(url)
        self.click("#explore-the-covid-data-from-our-world-in-data > div:nth-child(1) > span:nth-child(2) > a:nth-child(1)")
        self.switch_to_window(1)
        self.assert_title("Our World in Data · GitHub")

# Test currently disabled because it does not work reliable with 
class ScreenShotTest(BaseCase):
    def test_basic(self):
        self.open(url)
        time.sleep(20)  # give leaflet time to load from web
        self.set_window_size(800, 600)
        self.save_screenshot("current-screenshot.png")

        # test screenshots look exactly the same
        original = cv2.imread(
            "tests/data/test-screenshot.png"
        )
        duplicate = cv2.imread("current-screenshot.png")

        assert original.shape == duplicate.shape

        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
        assert cv2.countNonZero(b) == cv2.countNonZero(g) == cv2.countNonZero(r) == 0


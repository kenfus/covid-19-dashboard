from seleniumbase import BaseCase
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


class CovidDataExist(BaseCase):
    def test_basics(self):
        self.open("https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv")
        self.assert_no_404_errors()

class LongLatDataExist(BaseCase):
    def test_basics(self):
        self.open("https://gist.githubusercontent.com/cpl/3dc2d19137588d9ae202d67233715478/raw/3d801e76e1ec3e6bf93dd7a87b7f2ce8afb0d5de/countries_codes_and_coordinates.csv")
        self.assert_no_404_errors()


# Test is disabled because somehow, locally the screenshot has the wrong size of 454xN. However, on Github, the Sreenshot is always 450xN (correct). Thus, it needs figuring out why this is.
"""
class ScreenShotTest(BaseCase):
    # Test is pretty pointless because of GitHub "low resolution" virtual boxes for automatic testing.
    def test_basic(self):
        self.open(url)
        time.sleep(20)  # give leaflet time to load from web
        self.set_window_size(450, 450)
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
"""


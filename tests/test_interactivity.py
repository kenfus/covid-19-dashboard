from seleniumbase import BaseCase
import cv2
import time

##PARAMS FOR TESTS
url = "http://localhost:8501"




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


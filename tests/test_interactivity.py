from seleniumbase import BaseCase

class Global_View(BaseCase):
    def test_basics(self):
        url = "http://localhost:8501"
        self.open(url)
        self.assert_no_404_errors() 
        self.assert_title("main · Streamlit")
        self.assert_text("Our World in Data")
        self.assert_text("Albania: Total cases.", timeout=30)
        self.click("div.block-container:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > svg:nth-child(1)")
        self.click_xpath("/html/body/div[1]/div[2]/div/div/div[3]/div/div/div/ul/div/div/li[7]/span")
        self.assert_text("Global View: Total cases per million", timeout=30)
        self.assert_element_present(".stPlotlyChart")
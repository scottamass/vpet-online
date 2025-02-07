from appium_test import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_google_search_on_safari():
    # Appium server URL
    appium_server_url = "http://127.0.0.1:4723/wd/hub"

    # Desired capabilities for the iOS device or simulator
    desired_capabilities = {
        "platformName": "iOS",
        # "platformVersion": "16.0",  # Replace with your iOS version
        "deviceName": "8880B41E-05E7-4A25-81D8-7D0677D36B28",  # Replace with your device name or simulator
        "browserName": "Safari",
        "automationName": "XCUITest"
    }

    # Initialize the Appium driver
    driver = webdriver.Remote(appium_server_url, desired_capabilities)

    try:
        # Open Google in Safari
        driver.get("https://www.google.com")

        # Wait for the search box to load
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        # Enter "hello" into the search box
        search_box.send_keys("hello")

        # Submit the search form
        search_box.submit()

        # Wait for the results to load and confirm the search worked
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        print("Search completed successfully!")

    finally:
        # Quit the driver
        driver.quit()

if __name__ == "__main__":
    test_google_search_on_safari()

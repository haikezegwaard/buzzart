import urllib
from selenium import webdriver


def store_remote_image(url, xpath, target_file):
    """
    Fetch image from a remote url and  store it as
    a local asset. Image is retrieved via nodejs / selenium-webdriver
    Args:
        url: string, location of remote img (e.g. 'http://buzzart.django-dev.fundament.nl/digest/2')
        xpath: string, xpath identifier of img in html (e.g. '//div[@id="availability_plot"]/img' )
        target_file: string, name of file to save (e.g. 'my_img.png')
    """

    driver = webdriver.PhantomJS()  # or add to your PATH
    #driver.set_window_size(1024, 768)  # optional
    driver.get(url)
    # get the image source
    img = driver.find_element_by_xpath(xpath)
    src = img.get_attribute('src')

    # download the image
    return urllib.urlretrieve(src, target_file)



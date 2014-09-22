import urllib
from selenium import webdriver
from datetime import datetime
import logging
import os, errno

def store_remote_images(url, xpaths_files):
    """
    Fetch image from a remote url and  store it as
    a local asset. Image is retrieved via nodejs / selenium-webdriver
    Args:
        url: string, location of remote img (e.g. 'http://buzzart.django-dev.fundament.nl/digest/2')
        xpath_files: array of tuples, [(xpath identifier of img in html, target path of file)]
    """
    logger = logging.getLogger(__name__)
    driver = webdriver.PhantomJS()  # or add to your PATH
    # driver.set_window_size(1024, 768)  # optional
    driver.get(url)

    for (xpath, filename) in xpaths_files:
        # get the image source
        logger.debug("trying to fetch image: {} to file {}".format(xpath, os.path.dirname(os.path.abspath(filename))))
        mkdir_p(os.path.dirname(os.path.abspath(filename)))
        img = driver.find_element_by_xpath(xpath)
        src = img.get_attribute('src')
        # download the image
        urllib.urlretrieve(src, filename)

    return "fetched all images"


def date_to_datetime(date):
    """
    Convert date object to datetime object,
    adding midnight as time
    Args:
        date: date, date object to convert
    """

    return datetime.combine(date, datetime.min.time())

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

import urllib
from selenium import webdriver
from datetime import datetime
import logging
from settings import defaults
import os
import errno

logger = logging.getLogger(__name__)


def store_remote_images(url, summary_id):
    """
    Fetch image from a remote url and  store it as
    a local asset. Image is retrieved via nodejs / selenium-webdriver
    Args:
        url: string, location of remote img
        (e.g. 'http://buzzart.django-dev.fundament.nl/digest/2')
        xpath_files: array of tuples,
        [(xpath identifier of img in html, target path of file)]
    """
    logger = logging.getLogger(__name__)
    driver = webdriver.PhantomJS()  # or add to your PATH

    driver.set_window_size(1024, 768)  # optional
    driver.get(url)

    for img_item in driver.find_elements_by_xpath('//img'):
        parent_div = img_item.find_element_by_xpath('..')
        name = parent_div.get_attribute('id')
        file = '{}/{}.png'.format(summary_id, name)
        absolute_file = os.path.join(defaults.MEDIA_ROOT, file)
        mkdir_p(os.path.dirname(absolute_file))
        src = img_item.get_attribute('src')
        # download the image
        urllib.urlretrieve(src, absolute_file)

    return "fetched all images"


def date_to_datetime(date):
    """
    Convert date object to datetime object,
    adding midnight as time
    Args:
        date: date, date object to convert
    """

    return datetime.combine(date, datetime.min.time())


def datestr_to_datetime(datestr):
    """
    Convert string like "YYYYMMDD" to datetime object
    """
    return datetime.strptime(datestr, "%Y%m%d")


def mkdir_p(path):
    try:
        logger.debug("trying to make dir (mkdir -p): {}".format(path))
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            logger.debug("directory already exists, skipping")
            pass
        else:
            logger.debug("error creating directory")
            raise


def project_score(sold_count, interest_count, conversion_rate):
    """
    Calculate a project score: (sold houses / interest + conversion_rate) * 10
    This is for now, formula should  be more extensive
    and holding more variables
    """
    return ((sold_count / interest_count) + conversion_rate) * 10

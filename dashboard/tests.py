from django.test import TestCase
from pysimplesoap.simplexml import SimpleXMLElement
import logging

# Create your tests here.
class DashboardTest(TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)


    def test_convert_subscription(self):
        subscription = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?><subscription>
                        <id>181398</id>
                        <project externalId="003044" forSale="true">Appartementenvilla's Hofpark te Schagen</project>
                        <projectowner id="450">Bot Bouw Initiatief</projectowner>
                        <posted>201410210905</posted>
                        <domain>hofpark-schagen.php-dev.fundament.nl</domain>
                        <interests>
                            <interest selected="true">
                                <housetype externalId="GEN_D8EFF5F8-9806-43FF-A6F3-FC1682AA5D53">A2</housetype>
                                <housemodel id="4">Appartement</housemodel>
                                <pricemin>645000</pricemin>
                                <pricemax>645000</pricemax>
                            </interest>
                            <interest selected="true">
                                <housetype externalId="GEN_F6A95645-8B14-419D-9264-8D224D5E0BC0">C1</housetype>
                                <housemodel id="4">Appartement</housemodel>
                                <pricemin>373500</pricemin>
                                <pricemax>376000</pricemax>
                            </interest>
                            <interest selected="true">
                                <housetype externalId="GEN_715270A7-3957-4C20-807F-2786865AF579">C3</housetype>
                                <housemodel id="4">Appartement</housemodel>
                                <pricemin>565000</pricemin>
                                <pricemax>565000</pricemax>
                            </interest>
                            <interest selected="true">
                                <housetype externalId="GEN_3E5ECEEB-4870-4479-B892-D59887AC34AD">B1</housetype>
                                <housemodel id="4">Appartement</housemodel>
                                <pricemin>353500</pricemin>
                                <pricemax>362500</pricemax>
                            </interest>
                            <interest selected="true">
                                <housetype externalId="GEN_28F2D9F5-0FD2-4FB5-932F-EF3D0CA1D879">A1</housetype>
                                <housemodel id="4">Appartement</housemodel>
                                <pricemin>367000</pricemin>
                                <pricemax>376000</pricemax>
                            </interest>
                        </interests>
                        <subscribers>
                            <subscriber type="subscriber">
                                <id>425584</id>
                                <initials>N</initials>
                                <surname>Doorn</surname>
                                <street>KPC de Bazelweg</street>
                                <streetnumber>2</streetnumber>
                                <streetnumberaddition/>
                                <zipcode>1703DJ</zipcode>
                                <city>HHW</city>
                                <country>NL</country>
                                <phonenumber>0652092098</phonenumber>
                                <email>n.vandoorn@botbouwinitiatief.nl</email>
                                <gender>M</gender>
                            </subscriber>
                            <subscriber type="partner">
                                <id>425583</id>
                                <streetnumberaddition/>
                            </subscriber>
                        </subscribers>
                    </subscription>""")
        self.logger.debug('subscription date: {}'.format(subscription.posted))
        self.assertIsNotNone(subscription.posted, 'posted was None')

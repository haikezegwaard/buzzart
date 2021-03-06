from pysimplesoap.client import SoapClient
from monitor.models import InterestProject
from monitor.models import Project
import hashlib
import logging
from pysimplesoap.simplexml import SimpleXMLElement
import xml.etree.ElementTree as ET


class InterestManager:

    logger = logging.getLogger(__name__)

    def __init__(self):
        #LIVE
        self.client = SoapClient(
                            location = "https://xml.niki.nl/services/soap/interest",
                            action = 'https://xml.niki.nl/services/soap/interest', # SOAPAction
                            namespace = "http://endpoint.interest.service.lnp.fundament.nl",
                            soap_ns='soap', ns = False)

        #ACCEPTATIE
        #self.client = SoapClient(
        #                    location = "http://acc.niki.nl/services/soap/interest",
        #                    action = 'http://acc.niki.nl/services/soap/interest', # SOAPAction
        #                    namespace = "http://endpoint.interest.service.lnp.fundament.nl",
        #                    soap_ns='soap', ns = False)


    #return all subscribers from a list as one big xml document
    def getSubscriptionsAsDocument(self, interestAccount, idlist):
        total = ET.fromstring('<?xml version="1.0" encoding="UTF-8"?><subscriptions></subscriptions>') #returns root Element!
        for entry in idlist:
            tree = self.getById(interestAccount, entry)
            if total is None:
                total = tree
            else:
                total.append(tree)
        return total

    #
    # Niki Interest SOAP API method implementations
    #

    #return list of subscription ids  for given project, starting from given  date
    def getIdsByProjectFrom(self, interestAccount, projectId, from_date):
        pwd = hashlib.md5(interestAccount.password).hexdigest()
        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
              <getAllByProjectsFrom soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:end="http://endpoint.interest.service.lnp.fundament.nl">
         <username xsi:type="xsd:string">{}</username>
         <password xsi:type="xsd:string">{}</password>
         <projects xsi:type="end:ArrayOfProjectReference">
             <project xsi:type="end:ProjectReference">
             <projectId xsi:type="xsd:string">{}</projectId>
             </project>
         </projects>
         <start xsi:type="xsd:dateTime">{}</start>
      </getAllByProjectsFrom>
""".format(interestAccount.username, pwd, projectId, from_date.isoformat())) # manually make request msg
        response = self.client.call('getAllByProjectsFrom',params)
        result = response.getAllByProjectsFromResponse
        idlist = []
        for item in result.getAllByProjectsFromReturn:
                idlist.append(str(item))
        idlist = filter(None,idlist)
        return idlist

    #return list of subscription ids  for given project, starting from given  date, until given enddate
    def getIdsByProject(self, interestAccount, projectId):
        pwd = hashlib.md5(interestAccount.password).hexdigest()
        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
              <getAllByProjects soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:end="http://endpoint.interest.service.lnp.fundament.nl">
         <username xsi:type="xsd:string">{}</username>
         <password xsi:type="xsd:string">{}</password>
         <projects xsi:type="end:ArrayOfProjectReference">
             <project xsi:type="end:ProjectReference">
             <projectId xsi:type="xsd:string">{}</projectId>
             </project>
         </projects>
      </getAllByProjects>
""".format(interestAccount.username, pwd, projectId)) # manually make request msg
        response = self.client.call('getAllByProjects',params)
        result = response.getAllByProjectsResponse
        idlist = []
        for item in result.getAllByProjectsReturn:
                idlist.append(str(item))
        idlist = filter(None,idlist)
        return idlist

    def getIdsByProjectBetween(self, interestAccount, projectId, from_date, to_date):
        pwd = hashlib.md5(interestAccount.password).hexdigest()
        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
              <getAllByProjectsBetween soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:end="http://endpoint.interest.service.lnp.fundament.nl">
         <username xsi:type="xsd:string">{}</username>
         <password xsi:type="xsd:string">{}</password>
         <projects xsi:type="end:ArrayOfProjectReference">
             <project xsi:type="end:ProjectReference">
             <projectId xsi:type="xsd:string">{}</projectId>
             </project>
         </projects>
         <start xsi:type="xsd:dateTime">{}</start>
         <end xsi:type="xsd:dateTime">{}</end>
      </getAllByProjectsBetween>
""".format(interestAccount.username, pwd, projectId, from_date.isoformat(), to_date.isoformat())) # manually make request msg
        response = self.client.call('getAllByProjectsBetween',params)
        result = response.getAllByProjectsBetweenResponse
        idlist = []
        for item in result.getAllByProjectsBetweenReturn:
                idlist.append(str(item))
        idlist = filter(None,idlist)
        return idlist



    #get all subscription ids for account
    def getAll(self, interestAccount):
        pwd = hashlib.md5(interestAccount.password).hexdigest()
        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
              <getAll soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:end="http://endpoint.interest.service.lnp.fundament.nl">
         <username xsi:type="xsd:string">{}</username>
         <password xsi:type="xsd:string">{}</password>

      </getAll>
""".format(interestAccount.username, pwd)) # manually make request msg
        response = self.client.call('getAll',params)
        result = response.getAllResponse
        idlist = []
        for item in result.getAllReturn:
                idlist.append(str(item))
        idlist = filter(None,idlist)
        return idlist


    #get subscription ids for account from date
    def getFrom(self, interestAccount, date):
        pwd = hashlib.md5(interestAccount.password).hexdigest()
        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
              <getFrom soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:end="http://endpoint.interest.service.lnp.fundament.nl">
         <username xsi:type="xsd:string">{}</username>
         <password xsi:type="xsd:string">{}</password>
         <start xsi:type="xsd:dateTime">{}</start>
      </getFrom>
""".format(interestAccount.username, pwd, date.isoformat())) # manually make request msg
        response = self.client.call('getFrom',params)
        result = response.getFromResponse
        idlist = []
        for item in result.getFromReturn:
                idlist.append(str(item))
        idlist = filter(None,idlist)
        return idlist

    #get single subscription by id,
    #returns SimpleXMLElement
    def getById(self, interestAccount, subscriber_id):
        pwd = hashlib.md5(interestAccount.password).hexdigest()
        params = SimpleXMLElement("""<?xml version="1.0" encoding="UTF-8"?>
              <getById soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:end="http://endpoint.interest.service.lnp.fundament.nl">
         <username xsi:type="xsd:string">{}</username>
         <password xsi:type="xsd:string">{}</password>
         <id xsi:type="xsd:Long">{}</id>
      </getById>
""".format(interestAccount.username,pwd, subscriber_id)) # manually make request msg
        response = self.client.call('getById',params)
        result = unicode(response.getByIdResponse.getByIdReturn)
        logging.warn(result)
        return ET.fromstring(result.encode('UTF-8'))



    #get full subscriptions by array of ids
    def getByIds(self, interestAccount, ids):
        """
        Returns array of SimpleXMLElements
        """
        if ids is None:
            raise Exception('no array of ids given as input')
        if len(ids) == 0:
            raise Exception('array size of input ids was 0')
        pwd = hashlib.md5(interestAccount.password).hexdigest()
        xml_str = """<?xml version="1.0" encoding="UTF-8"?>
              <getByIds soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:end="http://endpoint.interest.service.lnp.fundament.nl">
         <username xsi:type="xsd:string">{}</username>
         <password xsi:type="xsd:string">{}</password>
         <ids xsi:type="end:ArrayOf_xsd_long">""".format(interestAccount.username, pwd)
        for entry in ids:
            xml_str += '<id xsi:type="xsd:Long">{}</id>'.format(entry)
        xml_str += '</ids></getByIds>'
        params = SimpleXMLElement(xml_str)
        response = self.client.call('getByIds', params)
        result = []
        if response.getByIdsResponse.getByIdsReturn is not None:
            for subscribtion in response.getByIdsResponse.getByIdsReturn.getByIdsReturn:
                uni = unicode(subscribtion)
                result.append(SimpleXMLElement(uni.encode('UTF-8')))
        return result

    def get_count_by_housetype(self, project, start, end):
        """
        Return a dictionary containing housetype names and the number of according
        interests for the given project between start and enddate
        """
        subscriptions = self.getByProjectBetween(project, start, end)
        occurrences = {}
        for subscription in subscriptions:
            root = ET.fromstring(subscription.as_xml())
            for housetype in root.iter('housetype'):
                if housetype.text in occurrences:
                    occurrences[housetype.text] += 1
                else:
                    occurrences[housetype.text] = 1
        allcount = len(subscriptions)
        speccount = 0
        for key, value in occurrences.iteritems():
            speccount += value
        occurrences['notype'] = allcount - speccount
        return occurrences


    #
    # Helper sheibe
    #
    def get_count_for_project(self, project):
        """
        Return count of subscribers for given project
        """
        nip = self.getNikiInterestProjectByProject(project)
        ids = self.getIdsByProject(nip.interestAccount, nip.nikiProjectId)
        return len(ids)

    def getByProjectBetween(self, project, start, end):
        """
        Return subscribers for a given project between start and end date
        """
        nip = self.getNikiInterestProjectByProject(project)
        ids = self.getIdsByProjectBetween(nip.interestAccount, nip.nikiProjectId, start, end)
        return self.getByIds(nip.interestAccount, ids)

    #helper lookup function
    def getNikiInterestProjectByProject(self, project):
        self.logger.debug('trying to fetch interestaccount by project id: {}'.format(project.id))
        try:
            return InterestProject.objects.get(project = project)
        except InterestProject.DoesNotExist:
            return None

    #Loop through subscriptions xml, and create a dictionary of
    #Housetype -> occurrences, the number of  preferred interests per housetype
    def mapSubscriptionDocumentToTypCountDictionary(self, document):
        #count subscriptions per housetype
        occurrences = {}
        root = document
        for subscription in root.iter('subscription'):
            for interest in subscription.find('interests').iter('interest'):
                if interest.find('housetype').text not in occurrences:
                    occurrences[interest.find('housetype').text] = 0
                if interest.get('selected') == 'true':
                    occurrences[interest.find('housetype').text] += 1
        return occurrences




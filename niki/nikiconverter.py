import requests
import logging


class NikiConverter:
    """
    Class to convert Niki data to the numbers needed
    static for now, should be replaced by oauth security model
    """
    oauth_token = "5060cbaf-35f5-41fe-9792-3c0c30012b7d"
    api_url = "https://api.niki.nl"

    availability = []

    def getProject(self, project):
        return self.apiRequest(project)

    def getHousesForSaleOrRent(self, project):
        self.getAvailability(project)
        return self.availability[0]

    def getHousesUnderOption(self, project):
        self.getAvailability(project)
        return self.availability[1]

    def getHousesSoldOrRented(self, project):
        self.getAvailability(project)
        return self.availability[2]

    def getAvailability(self, project):
        """
        check project status
        """
        projectJson = self.apiRequest(project)
        if projectJson.get('status') not in ("In verkoop",
                                             "In verhuur",
                                             "In verkoop / verhuur"):
            return None

        projectType = self.getProjectSaleRentType(project)
        # reset counters [forsale/rent, option, sold/rented]
        self.availability = [0, 0, 0]
        # get housetypes of project
        for housetype in self.apiRequest(project+"/housetypes"):
            if housetype.get('houses') is None:
                continue
            # get number for sale/for rent
            forSaleOrRent = housetype.get('houses').get(projectType)
            if(forSaleOrRent is not None):
                self.availability[0] += int(forSaleOrRent)
            # get number of houses under option
            underOption = housetype.get('houses').get('option')
            if(underOption is not None):
                self.availability[1] += int(underOption)
            # get number of houses sold or rented
            soldRentedStr = 'sold'
            if(projectType == 'for-rent'):
                soldRentedStr = 'rented'
            soldRented = housetype.get('houses').get(soldRentedStr)
            if(soldRented is not None):
                self.availability[2] += int(soldRented)
        return self.availability

    def getLabeledAvailability(self, project):
        projectType = self.getProjectSaleRentType(project)
        self.getAvailability(project)
        result = {}
        if(projectType == 'for-rent'):
            result = {'te huur': self.availability[0],
                      'optie': self.availability[1],
                      'verhuurd': self.availability[2]}
        else:
            result = {'te koop': self.availability[0],
                      'optie': self.availability[1],
                      'verkocht': self.availability[2]}
        return result

    def getProjectSaleRentType(self, project):
        projectJson = self.apiRequest(project)
        saleRent = 'for-sale'
        if(projectJson.get('type') == 'huur'):
            saleRent = 'for-rent'
        return saleRent

    def getHouseTypes(self, project):
        """
        Return all housetypes of given project
        """
        resource = project+"/housetypes"
        return self.apiRequest(resource)

    def getAllProjects(self):
        """
        Return list of all projects for given token
        """
        resource = "/search/projects"
        return self.apiRequest(resource)

    def apiRequest(self, resource):
        """do the request, append oauth token"""
        if(isinstance(resource, int)):
            logging.error("int: {}".format(resource))
        url = self.api_url + resource + "?oauth_token=" + self.oauth_token
        logging.warn("api call to: " + url)
        r = requests.get(url)
        return r.json()
# Buzzart #

## What is Buzzart? ##
Buzzart is a Django application ment to connect to external data sources / API's, and provide means to display this data in a meaningfull way. For example plotting gathered data in a dashboard.

## Supported datasources ##

Buzzart currently supports the following datasources:

1. Google Reporting / Google Metadata: enabling access to Google Analytics data
2. Facebook Graph API: providing insights for Fanpages
3. Mailchimp API: providing list and campaign statistics
4. Niki API: providing woningaanbod
5. Niki Interest API: providing subscriber information per project
6. Twitter API: providing access to Twitter API
7. Facebook Ads API: providing campaign statistics
8. Google Ads API: (work in progress) providing campaign statistics

## Supported views ##

1. Buzzart can generate data formatted for usage in Cyfe, a third party dashboarding system. It can be included using the 'private url' widget. Main url entry point for this view is http://buzzartdomain/cyfe
2. Buzzart can generate mailings containing plots (images generated from interactive plots) plus contextual advise (provided by hand.) These advisory mailings are semi-automaticly generated over a given time span. Entry point: http://buzzartdomain/digest/{summary-id}. Mailings are sent by [mandrill](http://www.mandrill.com), a transactional mailing service.
3. Buzzart can display gathered data in a dashboarding environment. Dashboard template is based on ([sb-admin-2](http://startbootstrap.com/template-overviews/sb-admin-2/)

## Plotting data ##

For the plotting of data, initially the Google Visualisation API was used. In the dashboard environment however, Buzzart uses [highcharts](http://www.highcharts.com) as a plotting library because of a nicer interface and a lot of options and variations.

## Setting up ##

### Installation ###


```
#!bash

git clone https://fundamentallmedia@bitbucket.org/fundamentallmedia/buzzart.git
cd buzzart
pip install -r requirements.txt
python manage syncdb
python manage migrate
python manage runserver
```

### Google Analytics API ###

1. Make sure you have setup a project setup in your Google Developer Console https://console.developers.google.com
2. Enable 'analytics api'
3. Configure settings.py:


```
#!python

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = CLIENT_ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = CLIENT_SECRET
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type': 'offline'}
```

Finally as superuser, access http://buzzartdomain/login/google-oauth2?next=/ , it will fetch an oauth token and link it to the current user.

### Facebook Graph API Fanpages ###

1. As superuser, access http://buzzartdomain/login/facebook?next=/ , it will fetch an oauth token and link it to the current user.
2. Be sure the linked facebook user is administrator of the configured fanpage ids per project.
3. Go to the index page http://buzzartdomain/ and push 'Update facebook tokens fanpages'. It will gather a never expiring access token for each of the configured fanpages.

### Mailchimp API ###

1. Create a Mailchimp API token for the mailchimp account you want to access.
2. Get the List Id from your Mailchimp account
3. Test the setup by calling http://buzzartdomain/cyfe/mailchimp/?apikey={api_key}&lid={list_id}
4. Enter the API token and List Id for your project

### Niki API ###

1. Retrieve an Oauth1 token for your application. (At the moment a key is hardcoded in Buzzart)
2. Test the connection by calling http://buzzartdomain/niki/projects, this will retrieve a list of all projects available for your token.
3. Configure the resource (from the above response) for your project

### Facebook Ads API ###

1. Create and configure a facebook app
2. Configure FACEBOOK_ADS_APP_ID, FACEBOOK_ADS_APP_SECRET and FACEBOOK_ADS_ACCESS_TOKEN in settings.py
3. The access token can be obtained using the graph api explorer https://developers.facebook.com/tools/explorer/
4. Make sure your facebook app has 'app secret proof' enabled
5. Permissions for the ACCESS_TOKEN should include 'manage_ads'
6. Test your setup by accessing http://buzzartdomain/fbads
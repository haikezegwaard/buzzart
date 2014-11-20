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
2. Buzzart can generate mailings containing plots (images generated from interactive plots) plus contextual advise (provided by hand.) These advisory mailings are semi-automaticly generated over a given time span. Entry point: http://buzzartdomain/digest/{summary-id}
3. Buzzart can display gathered data in a dashboarding environment. Dashboard template is based on ([sb-admin-2](http://startbootstrap.com/template-overviews/sb-admin-2/)
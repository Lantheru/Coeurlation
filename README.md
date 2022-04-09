# Coeurlation 

Requires the following modules:
-psycopg2
-pandas
-numpy
-requests
-json
-csv
-re

Synopsis:
The goal of the Coeurlation project is to establish and curate a Postgres database that takes market data for the FFXIV Crystal datacenter from the universalis.app API so that it can be analyzed for trends and detects abnormal market behavior. This is being done by a junior programmer as a part of a learning exercise, so included will be notes on approaches to the projects goals as well as learning experiences. Note that many importable modules that would trivialize this task are being deliberately ignored in order to delve into a deeper understanding of each facet of the entire process of building a complete application. This means that the evolution of the code as I become more familiar with different concepts may not be as elegant.

Universalis, which we'll abbreviate to Uni' going forward, consolidates information taken from players who use their supporting plugin and relays useful information about market prices, supply/demand ratio, and most recent transactions. There is more that can be done with the raw data, but some of the data sets that would be required to come to accurate conclusions aren't directly callable via their web interface. For instance, some players deliberately take advantage of how both Uni' and the FFXIV market board only display a fixed number of the most recent transactions in order to deceive buyers who are unaware of the actual market for a given item. It would be possible to detect these attempts at market manipulation and automate a notification. Additionally, because it is possible to purchase items in other worlds for resale in our home server of Coeurl, it is possible to detect for significant differences in price to generate profit via arbitrage.

The subgoals of the project are as follows:
-Automate a method to obtain relevant data from Uni' and update another database with it. This will involve querying multiple API and adjust parameters dynamically as events are detected.
-Design methods to query from our database and organize the information for analysis in Python.
-Automate detection of notable events and arrange scripted notification via Discord bot.
-Categorize events and submit to database for later analysis
-Later reformat code to reflect PEP 8 style
-As added...

Development and Learning:
## Database


Complications:
-Item/IDs riddled with spaces, apostrophes, and japanese text. Made porting over to sql difficult since they'd need to be preserved through transfer for use in making requests to API. Needed to change encoding for postgres to interpret unexpected characters.
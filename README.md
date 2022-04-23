# Coeurlation 
\n\n\n



Synopsis:
The goal of the Coeurlation project is to establish and curate a Postgres database that takes market data for the FFXIV Crystal datacenter from the universalis.app API so that it can be analyzed for trends and detects abnormal market behavior. This is being done by a junior programmer as a part of a learning exercise, so included will be notes on approaches to the projects goals as well as learning experiences. Note that many importable modules that would trivialize this task are being deliberately ignored in order to delve into a deeper understanding of each facet of the entire process of building a complete application. This means that the evolution of the code as I become more familiar with different concepts may not be as elegant.\n 

Universalis, which we'll abbreviate to Uni' going forward, consolidates information taken from players who use their supporting plugin and relays useful information about market prices, supply/demand ratio, and most recent transactions. There is more that can be done with the raw data, but some of the data sets that would be required to come to accurate conclusions aren't directly callable via their web interface. For instance, some players deliberately take advantage of how both Uni' and the FFXIV market board only display a fixed number of the most recent transactions in order to deceive buyers who are unaware of the actual market for a given item. It would be possible to detect these attempts at market manipulation and automate a notification. Additionally, because it is possible to purchase items in other worlds for resale in our home server of Coeurl, it is possible to detect for significant differences in price to generate profit via arbitrage.\n\n

The subgoals of the project are as follows:\n
-Automate a method to obtain relevant data from Uni' and update another database with it. This will involve querying multiple API and adjust parameters dynamically as events are detected.\n
-Design methods to query from our database and organize the information for analysis in Python.\n
-Automate detection of notable events and arrange scripted notification via Discord bot.\n
-Categorize events and submit to database for later analysis\n
-Later reformat code to reflect PEP 8 style\n
-As added...

Development and Learning:
## Database\n
-Database is currently a simple postgres database with tables corresponding to Scraper's functions and preloaded item/world lists. Once collection of data is automated and set to repeat at certain time intervals the idea is to filter out redundant information and develop scripts that further refine our data to trigger events and export for visualization via premade tables and the discord bot.\n

## Automation\n
-Due to the large amounts of potential data these tables can bring up I needed to find a way to bypass discord's 2000 character limit. After importing a module to convert my dataframes into image files I was writing them to a folder and reading them into discord's message function. This was taking longer than I wanted it to (partially due to the data pipeline not being optimized, but also because I was transforming/writing/reading too much data from disk) so figured out how to omit the writing process by porting it through memory.\n\n

-After wrestling with formatting the dataframes to be inserted into our database, we can now call a function to pull a list of predefined items from a list of predefined worlds (currently defaulting to all servers in the Crystal datacenter) and insert them into a single table in the database which should be easier to filter using SQL. Implementing a method to scrape Uni's history data over will be significantly more challenging seeing as the historical data for all transactions of certain items for all eight servers may produce problematic requests. Will have to go over the API's limits to estimate what will be needed for this problem.\n\n

-Since the discord bot was made prior to the method in which we'll be updating information into the database, there is an issue in that there are several transformations of the data that aren't necessary for updating the tables and we can better optimize flow by reordering so that the database updates and filters itself and redesignates the discord bot to pull its information from locally formed tables instead of the api. While salehistory seems to be uploading fine, current listings seem to be displaying too much redundant information and will need to be looked at to ensure that the data isn't being unintentionally altered before it gets to the db.\n\n

-The update task creates a queue and multiple threads to insert into the database, mostly as a way to mitigate the time it takes to create dataframes, but for the sake of optimization I plan to omit that step to separate data engineering tasks from data analysis. 


Complications:\n
-Item/IDs riddled with spaces, apostrophes, and japanese text. Made porting over to sql difficult since they'd need to be preserved through transfer for use in making requests to API. Needed to change encoding for postgres to interpret unexpected characters.\n

-It seems that certain information available on Uni's web page isn't available through their provided API (namely the player names from sales transactions) and so obtaining complete information may require scraping the site.
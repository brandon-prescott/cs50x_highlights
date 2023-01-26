# Jobs

#### Description:

This program is a web scraper that is able to extract summary information from software related job postings, such as the job title, location and programming languages required. This allows users to quickly gather relevant information from multiple job listings at once, saving them valuable time and energy. This program could also be generalised to search for any key words in other types of job postings. Programming languages were just a good parsing challenge.

The scrape.py file starts by asking the user how many pages it wants them to scrape. I chose to add this in as a feature to help with development purposes, as it takes ~ 10 seconds to run per page that it needs to scrape. I think it would take ~ 1 hour to search the entirety of Reed's Software Engineering postings. It then starts looping through all of the job posting URLs and uses BeautifulSoup to extract information from each page. Once it has extracted the text from the job posting in a form that is usable, it checks each string against a global languages array that contains a list of all the programming languages to check for (web frameworks were not added to this list, as I wanted to keep it specific to core programming languages and database tools).

It then produces a dictionary summary for each job posting, containing: Job title, location, programming languages and the URL. The programming language data is stored as a 0 or 1 depending on whether the language exists in the posting or not, as this will also help a user with generating summary statistics. The data is written to both an SQL database and CSV file, depending on how someone might want to use the data for post-processing i.e. producing summary graphs in Excel or embedding the results in a web application using SQL.


Steps to run the program:

(1) Navigate to the program's directory in the terminal

(2) Ensure python is installed on your system, along with the following libraries: bs4, requests, csv, sqlite3

(3) Run the following command: **python3 scrape.py**

(4) Enter the number of pages you want to scrape (~10s per page)

(5) Check the output csv for the summary data, or run **sqlite3 jobs.db** to find the data in the db file



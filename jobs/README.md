# JOB SCRAPER

#### Description:

This web scraper is able to extract summary information from software related job postings, such as the job title, location and programming languages required. This allows users to quickly gather relevant information from multiple job listings at once, saving them valuable time and energy.

The scrape.py file starts by asking the user how many pages it wants them to scrape. I chose to add this in as a feature to help with development purposes, as it takes ~ 10 seconds to run per page that it needs to scrape. I think it would take ~ 1 hour to search the entirety of Reed's Software Engineering postings. It then starts looping through all of the job posting URLs and uses BeautifulSoup to extract information from each page. Once it has extracted the text from the job posting in a form that is usable, it checks each string against a global languages array that contains a list of all the programming languages to check for (web frameworks were not added to this list, as I wanted to keep it specific to core programming languages and database tools).

It then produces a dictionary summary for each job posting, containing: Job title, location, programming languages and the URL. The programming language data is stored as a 0 or 1 depending on whether the language exists in the posting or not, as this will also help a user with generating summary statistics. The data is written to both an SQL database and CSV file, depending on how someone might want to use the data for post-processing i.e. producing summary graphs in Excel or embedding the results in a web application using SQL.


The main function describes the high level activities the programming is executing:

initialise_database(): Connects to the SQL databse, creates a jobs summary table if it doesn't already exists, and clears any data from it if it already exists.

get_number_of_pages(): Gets the integer number of pages to scrape from the userand performs some input validation checks.

get_all_job_urls(number_of_pages): Takes the number of pages as an input and returns a list of every job posting URL that is found.

get_job_summary(job_url): Takes the current job posting URL as an input and returns a dictionary with summary data from the job posting.

write_to_database(job_summary): Takes in a single job posting dictionary and executes a database query to insert the job to the table.

write_to_csv(job_summary_list): Takes the list of all job postings and writes the same information to a CSV file.

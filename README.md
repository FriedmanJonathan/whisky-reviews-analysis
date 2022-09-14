# whisky-reviews-analysis
Scraping a bit of data from a whisky database and then conducting some NLP and ML anaylsis (in progress).

IMPORTANT: while the repository has the MIT license and you may do as you please with the code, the data itself (.csv) has been scraped from WhiskyBase taking into account Fair Use: this is a strictly personal project and I will not use their data for any commercial use, and neither should you.

There are currently two Python files:
**1. WhiskyBaseScraper.py** scrapes the WhiskyBase site and creates dataframes (and then CSVs) of distilleries, whisky attributes, and reviews.
This code showcases the classic **ETL** pipeline: iterative scraping of multiple layers of the website, and data cleaning in order to prepare the data for analysis.

**2. WhiskyReviewAnalysis.py** currently contains the ability to create a word-cloud (including having it in the shape of a glencairn glass!) and to find the most common words. It uses the CSVs which were created using the aforementioned scraping file.
This code showcase some common NLP methods: word clouds, vectorizers, and dealing with stop-words and unwanted common words.

Future work: 
1. Extract more features (such as proof/ABV, which is tricky due to the different formats)
2. Analyzing the reviews using TF-IDF, in order to further understand what makes whiskies unique.
3. Implementing a suggestion model would be awesome.
I'm sure there are other great ideas which I'll come up with on the fly, and I'm always open to suggestions!

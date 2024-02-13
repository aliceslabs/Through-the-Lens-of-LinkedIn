# Through-the-Lens-of-LinkedIn
## Programming Language and library
The crawler and website are developed using Python3. They depends on several third-party libraries.<br/>
Required libraries:
* pandas 
* numpy
* matplotlib
* selenium
* BeautifulSoup
* flask
* wordcloud
## Explantion of files and folder
1) config.txt<br/>
It stores the username and password of LinkedIn.
2) crawling.py<br/>
It crawls profiles of Queen's Computing alumni.
3) names.txt<br/>
It contains some popular names which are used by crawling.py.
4) profiles.csv<br/>
It stores crawled profiles.
5) presentation.py<br/>
It analyzes the profiles and display the result in the webpage.
6) templates<br/>
The folder holds the templates in Flask application.
7) static<br/>
The folder holds the static files in Flask application.
## Run
1) Crawler<br/>
Put you LinkedIn credentials in `config.txt` and then run the crawler using `python3 crawling.py`. You need to manually complete the verification of LinkedIn if necessary.
2) Website<br/>
Run the website using `python3 presentation.py` and then visit the link [http://localhost:5050](http://localhost:5050).

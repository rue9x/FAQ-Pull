# FAQ-Pull #

Syntax: python3 FAQ-pull.py [console] [game]


What is does:
Searches GameFAQs for the game you look for and downloads the "best" FAQ walkthrough for it. 

By "best", it rates them in the order of "Highest Rated", "Most Recommended", "Complete", and "Partial", in that order. It doesn't consider unrated FAQs, and it only searches the top "General FAQs" block (as that tends to be the section with general walkthroughs". 

Requirements:
- Python 3.6 or 3.7 (https://www.python.org/downloads/)
- Selenium ('pip install selenium' after you install python)
- Chromedriver (installed in PATH or c:\chromedriver\) (https://chromedriver.chromium.org/downloads, make sure you get the version that matches up with your version of Google Chrome)
- Google Chrome (http://google.com/chrome) (again, make sure you get the version that matches up with ChromeDriver)

This was designed for Windows usage, but it would likely also work in CentOS or Ubuntu.

Goals:
I do this kind of work for a living and I felt like making something like this at home on my off-day for fun. Eventually I might make this into a mobile app or add HTML support, speed it up, or add some stability, but for now I'm happy with it. If you enjoy it, send me a "thanks".

- (C) 2019 Rue Lazzaro
(rue dot lazzaro AT gee mail dot com)

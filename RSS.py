import re, requests
from bs4 import BeautifulSoup
from collections import Counter

def read_rss():
    url = 'https://feeds.feedburner.com/arstechnica/science'

    r = requests.get(url)
    # soup = BeautifulSoup(r, 'xml')

    # Find all the titles in the RSS feed
    # <title>Some title here</title>
    titles = re.findall('<title>(.*)</title>', r.text)
    for i, title in enumerate(titles):
        print(f'{i}\t{title}')


if __name__ == "__main__":
    with open('test.xml', 'rb') as f:
        rss = f.read()
    i = 0
    tags = []
    tmp = ''
    for ch in rss:
        if chr(ch) == '<':
            tmp = chr(ch)
            i += 1
        elif chr(ch) == ' ':
            i = 0
            continue
        elif i == 1 and chr(ch) == '/':
            i = 0
            continue
        elif i > 0 and chr(ch) == '>':
            tmp = tmp + chr(ch)
            tags.append(tmp)
            i = 0
            continue
        else:
            tmp = tmp + chr(ch)
            i += 1
    print(tags)

# Basic structure of Ars Technica RSS Feed
# <rss> is the main tag
# <channel> seems to 
#   a) give basic info on the feed and
#   b) contain <item> tags that encapsulate each article
# each item tag has
# <title>       The title of the article
# <link>        A link to the article (does not appear to be permanent link)
# <pubDate>     Publication date of the article
# <dc:creator>  Author of the article
# <category>    Labels the article with descriptive topic tags. There can be
#               more than one category per article. They follow the format:
#               <![CDATA[meta tag]]>
# <guid>        In this case, same as <link>
# <description> A brief description of the article. Same CDATA format as above
# <content:encoded> contains the first few sentences of the article. Same CDATA
#               as category data.


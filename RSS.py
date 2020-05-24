import feedparser
from collections import Counter

def read_rss(etag='44HV76Xhrz/fXa4SuqNYQBlOptw'):
    url = 'https://feeds.feedburner.com/arstechnica/science'

    # r = requests.get(url)
    # d = feedparser.parse(r.text)
    d = feedparser.parse(url, etag=etag)
    print('### START')
    if d.status != 304:
        print(d.feed.title)
        print(d.etag)
        print(len(d.entries))
        print(type(d.entries))

        for entry in d.entries:
            print(entry.title)
            print(f'\t{entry.link}')
            print(f'\t{entry.description}')
            print(f'\t{entry.published}')
            print(f'\t{entry.id}')
            print(f'\t{entry.tags}\n')
    

if __name__ == "__main__":
    read_rss()

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


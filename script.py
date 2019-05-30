import praw
import re

KEYS = ["speaker","earbuds","earphones","headphone","flash drive","adapter"
       ,"docking","sleeve","cover","keyboard","mouse"]

def main():
  reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     username='',
                     password='')
  

  subreddit = reddit.subreddit('macbookdeals')
  
  for submission in subreddit.stream.submissions(skip_existing=True):
    process_submission(submission,subreddit)
  

def process_submission(newSubmission,subreddit):

  title = newSubmission.title.lower()
  
  query = []
  
  searchString = ""

  macbook = re.findall("([0-9]gb ram)|([0-9]\sgb ram)", title)
  
  if macbook:
  
    if "macbook pro" in title:
      query.append("macbook pro")
    else:
      query.append("macbook air")
  
    searchString = query[0] + ' AND NOT docking AND NOT sleeve AND NOT adapter AND NOT cover'
    
  else:
  
    for word in KEYS:
      if word in title:
        query.append(word)
        break
  
    searchString = query[0]
  
    if ("sleeve" in query)or("case" in query)or("cover" in query):
      query = ["sleeve","cover"]
      seperator = ' OR '
      searchString = seperator.join(query)
  
  print(searchString)
  
  found = [submission for submission in subreddit.search(searchString,sort='new')]
  
  if len(found) > 0:
    REPLY_TEXT = "**Hi**, here are a few related **Deals** for you :\n"
  
    for submission in found[:3]:
      REPLY_TEXT += "- [" + submission.title + "]" + "("+submission.permalink + ") \n"
    
    REPLY_TEXT += " \n I'm a bot for [r/MacbookDeals](https://www.reddit.com/r/MacbookDeals/)"
    
  newSubmission.reply(REPLY_TEXT)  
  

    
if __name__ == "__main__":
    main()

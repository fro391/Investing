import praw

r = praw.Reddit(user_agent='kumaX')
#r.login('kumaX','Sho3lick')
submissions = r.get_subreddit('worldnews').get_top()
print [str(x) for x in submissions]


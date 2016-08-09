from secrets import USERNAME, PASSWORD
import os, praw, re


def bot():
    #  Initializes and logs in.
    r = praw.Reddit(user_agent='GPG Bot 0.1 by u/'+USERNAME)
    r.login(USERNAME, PASSWORD)

    #  Checks for a gpgkey dir. Makes one if one doesn't exist.
    if not os.path.exists('keys'):
        os.makedirs('keys')

    begin = '-----BEGIN PGP PUBLIC KEY BLOCK-----'
    end = '-----END PGP PUBLIC KEY BLOCK-----'

    #  Parses subreddit for keys
    subreddit = r.get_subreddit('gpgpractice')
    for post in subreddit.get_new():
        if begin in post.selftext and end in post.selftext:
            #  Key formatting
            starting_index = post.selftext.find(begin)
            key = post.selftext[starting_index:]
            ending_index = key.find(end)
            key = key[:ending_index] + end
            key = re.sub(r'[ ]{4}', '', key)
            #  If author doesn't have dir, make one
            if not os.path.exists('keys/'+str(post.author)):
                os.makedirs('keys/'+str(post.author))
            #  Write string to file every time (in case the file is edited)
            with open('keys/'+str(post.author)+'/'+str(post.id)+'.txt', 'w') as f:
                f.write(key)


bot()

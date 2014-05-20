import praw
import getpass
import time
import re

import context
import text_over_image
import SaveToFile

shoutout = re.compile('!stanbot.request')


def boot():

    version = '1.9'

    print('\nStanbot-5000, version: ' + version)
    print('------------------------------')

    user = raw_input('> Reddit Login: ')
    passwd = getpass.getpass("> {}'s password: ".format(user))
    agent = ('/u/{0} running Stanbot-5000, version: {1}'.format(user, version))

    r = praw.Reddit(user_agent=agent)
    r.login(user, passwd)

    theloop(user, r)


def theloop(user, r):

    cache = []

    print('\n> Starting up Stanbot-5000. \
        Notifications for requests will be printed')
    print('To stop, press Ctrl + C.')

    try:

        while True:

            inbox = None
            inbox = r.get_unread(limit=None)

            print('\n> Checking mailbox for messages...')

            for letter in inbox:
                try:
                    if "Stanbot, I found a bug!" in letter.subject:
                        print('\n> A wild bug appeared!')
                        print('=========================')
                        print(letter.body)
                        SaveToFile.save_to_file(letter.body, 'bug_tracker.txt')
                    elif "New Feature" in letter.subject:
                        print('\n> What? Stanbot-5000 is evolving!')
                        print('===================================')
                        print(letter.body)
                        SaveToFile.save_to_file(letter.body, 'feature_request.txt')
                        letter.reply('Thanks, sending the request to the dev.')
                    elif "+delete " in letter.body:
                        print('\n> A wild MissingNo. appeared!')
                        delete_thing = letter.body.replace('+delete ', '')
                        comment = r.get_info(thing_id='t1_' + delete_thing)
                        parent = r.get_info(thing_id=comment.parent_id)
                        if comment.author.name == user and parent.author.name == letter.author.name:
                            print('\n> Stanbot-5000 deployed a pokeball!')
                            try:
                                comment.delete()
                                print('\n> MissingNo. was caught!')
                                with open('comment_deletion.txt', 'r') as cdel:
                                    reply_text = cdel.read()
                                letter.reply(reply_text.format(comment.permalink))
                            except:
                                print('\n> Game Save was corrupted due to item clone hack!')
                                letter.reply('Sorry, but I\'m having trouble deleting the comment. Most likely because ***you aren\'t the parent commenter of the comment you want removed.\n\n'
                                    '*It could also be simply because /u/minecraftstan, the Lord of the Realm, hates you\n\n'
                                    '[^Think ^this ^is ^a ^big ^mistake?](http://www.reddit.com/message/compose?to=RamblingPirate&subject=Da%20Fuck?&message=')
                    else:
                        print('\n> Inbox fainted!')
                        print('====================')
                        print('Letters were junkmail.')
                except Exception as e:
                    print('\n> Inbox is poisoned! Inbox fainted.')
                    print('========================================')
                    print('There was an unexpected error while reading the mail:\n{}'.format(e))
                letter.mark_as_read()

            print('\n> Checking for stanism requests...')
            comments = r.get_comments('all+stanisms', limit=500)

            for comment in comments:

                condition, rquests = check(comment)
                subreddit = comment.subreddit.display_name
                # print('\n> now entering Elite Four Trainer: {}'.format(subreddit))

                if condition and comment.id not in cache:

                    print('\n> Valid stanism request found in /r/{}'.format(subreddit))
                    post(r, comment, rquests, cache)

            print('\n> Now Sleeping...')
            time.sleep(15)

    except KeyboardInterrupt:

        print('> Stopped Stanbot-5000. Thanks for playing.')

    except Exception as e:
        print('\n> Oh no! An error has occured. (Most likely a socket timeout)')
        print(e)
        print('\nRestarting...')
        theloop(user, r)


def check(comment):

    body = comment.body
    #print(re.findall(shoutout, body))
    rquests = set(re.findall(shoutout, body))
    condition = False

    if rquests:

        condition = True

    return condition, rquests


def parse_quote(text):
    thing = text.split(' ')
    if 'like' in thing:
        try:
            index = text.find(' like ')
            search = text.split(' [')[1].strip(']')
            temp = text.split(' [')[0]
            result = [temp[0:index+1], temp[index+1:len(temp)], search]
            return result
        except IndexError:
            return None

    elif 'as' in thing:
        try:
            index = text.find(' as ')
            search = text.split(' [')[1].strip(']')
            temp = text.split(' [')[0]
            result = [temp[0:index+1], temp[index+1:len(temp)], search]
            return result
        except:
            return None
    else:
        search_p = re.compile(r'\[.*\]')
        search = search_p.search(text).group().strip('[]')
        top, bottom = text.split()[:(len(text.split())+1)/2], text.split()[(len(text.split())+1)/2:]
        top_text, bottom_text = ' '.join(top), ' '.join(bottom).split(' [')[0]
        result = [top_text, bottom_text, search]
        return result


def post(reddit, comment, rquests, cache):

    for c in rquests:

        text = comment.body.split('&gt;')[1].strip(' ').split('\n')[0]

        result = parse_quote(text)
        top, bottom, search = result[0], result[1], result[2]
        context.get_image(search)
        time.sleep(.5)
        image = 'result_no_text.jpg'
        text_over_image.text_to_image(image, top, bottom)
        imgurlink = text_over_image.upload('result.png', top, search)

        with open('betaRequest_reply.txt') as text:
            comment_body = text.read()

        place_holder = comment.reply('Processing hyperbolic nanite algorithm...')
        cache.append(comment.id)
        reply_with = comment_body.format(imgurlink, place_holder.id)
        place_holder.edit(reply_with)

    return cache


boot()

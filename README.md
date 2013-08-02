# Twitter to App.net Crossposter
##### Version 1.0.1, released 08/02/2013
##### by Donald Burr <dburr@borg-cube.com>

### ChangeLog

##### Version 1.0.1, released 08/02/2013

* Fix handling of boolean values read from config files

##### Version 1.0.0, released 07/25/2013

* Initial release

### Purpose

This script allows you to crosspost your [Twitter][TWITTER] posts ("tweets")
to the new up-and-coming social network/app platform [App.net][APPDOTNET].
It was created because I wanted a quick and simple way to share content
to both services.  I simply don't have [over 9,000][OVER9000] hours in the day
to manage all these social networks, nor do I have the patience to do so.

In the past this task could be easily accomplished using a nifty service
called [If This Then That (IFTTT)][IFTTT].  However recently Twitter has
[blocked IFTTT access][TWITTER-BLOCKS-IFTTT] to the Twitter API, which
meant this method would no longer work.  I was able to find [a different
method][TWITTER-RSS] of piping Twitter data into IFTTT.  Unfortunately this
method had two downsides: all posts to App.net were prefixed with your
Twitter username, and also @mentions and retweets were carried over as
well.  But it worked well enough for my purposes.  Unfortunately, shortly
after I discovered it, Twitter [deprecated][TWITTER-RSS-DEPRECATED] their
RSS support, rendering this method non-functional as well.

My latest solution to this problem is this script, which directly calls
the Twitter API to read a user's posts.  As such it requires you to set up
developer accounts with both Twitter and App.net.

### Prerequisites

In order to use this script, you will need to install the following
Python modules, as well as their prerequisites.  Consult their Github
pages for instructions on how to do so.

* [Python][PYTHON] (tested with 2.6.6 and 2.7.2)
* [Python-Twitter][PYTHON-TWITTER]
* [Python App.net API Wrapper][PYTHON-APPDOTNET]
* [SimpleJSON][SIMPLEJSON]

You will also need to set up Developer Accounts with both [Twitter][TWITTERDEV]
and [App.net][APPDOTNETDEV].  In the case of Twitter, this is free; however
with App.net you will need to pay for a developer account, which costs
$100/year.

This script needs to run continuously, so you might want to consider
running it under a terminal multiplexer that supports detached sessions
such as [screen][SCREEN] or [tmux][TMUX].

### Setup

First, install the above prerequisites.  To test if everything is
configured properly, run

`python mirror.py --help`

You should see a help message (and, more importantly, no error
or warning messages).

Next, head over to the [Twitter developer center][TWITTERDEV], and
sign in with your Twitter credentials.  At the upper right of the
screen should be your user pic; click on it and a pulldown menu
will appear.  Choose "My Applications," then click "Create a new
application."  Fill in the requested information (you can use any
URLs for both the Website and Callback URL).  Once the app has been
created, look under "OAuth Settings" and make a note of your "Consumer
Key" and "Consumer Secret."  On the same page, look for the "Your
access token" section, and click "Create my access token."  Wait a few
minutes then refresh the page.  You should now see an "Access token"
and "Access token secret" appear; note down those values as well.
  
Now head on over to the [App.net Developer Center][APPDOTNETDEV] and create
a new app.  Again, you can fill in anything for Website and Callback
URL.  Once the app is created, scroll down to the "OAuth 2 Settings"
section and make a note of the "Client ID" and "Client Secret."
Scroll down to the "App Settings" section, and click the "Generate a
user token for yourself" link.  When asked for the scope, make sure
"write post" is checked.  Make a note of the token code that has been
generated for you.

Now make a copy of `config.sample`, open it in your favorite text editor,
and fill in the requested values.

Finally, run the script with:

`python mirror.py -c *config-file*`

Some other command-line arguments include:

```
Usage: mirror [-c | --config=configuration file (default: `mirror.cfg')]
              [-i | --poll-interval=period in secs between polls (default=300)
              [-m | --mirror-mentions]
              [-d | --mirror-indirect-mentions]
              [-r | --mirror-retweets]
              [-u | --user-to-mirror=username to mirror]
              [-n | --simulation-mode]
              [-v | --version]
```

Note that if an option is specified both in the configuration file as well
as a command-line argument, the command-line argument takes precedence.

### Future Plans

Some ideas for features/enhancements that I will try and implement.

* Option to crosspost @mentions if the user being @mentioned also has
  an account on App.net
* Mechanism to filter posts, that is, to prevent crossposting of posts
  that match certain criteria (regexp, client name, etc.)  This can be
  used, for example, to prevent crossposting of automatically generated
  tweets (from services such as Foursquare, GetGlue, etc.).

If you have any ideas for additinoal features or enhancements,
please feel free to [open an issue on Github][GHISSUES].
Or better yet, [fork this repo][GHFORK], add the feature/make the change,
and submit a pull request.

### About the Author

I'm a software engineer-for-hire living and working in the Santa Barbara,
California area.  I develop in many languages and have published a few apps
in the [iOS App Store][DBURRAPPS] (and soon hopefully the Mac App Store
and Google Play as well).

Find out more about me and read my technological musings over at
[my blog][DBURR].

I also run a podcast dedicated to Japanese animation (anime) as well as
other facets of Japanese pop culture, food, travel, and more.  You can
find that over at [Otaku no Podcast][OTAKU].

### Like what you see?

Unfortunately with the economy being the way it is, finding work has been
rather difficult, so if you like what you see here and are able to, a small
donation would be greatly appreciated.

[![Donate via PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=U4T93T9ZJNHM6)
[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=dburr&url=https://github.com/dburr/twitter_adn_mirror&title=twitter_adn_mirror&language=python&tags=github&category=software)

### License

This work is licensed under the [MIT License](LICENSE).

[TWITTER]: http://twitter.com "Twitter"
[TWITTERDEV]: https://dev.twitter.com "Twitter Developer"
[APPDOTNET]: https://alpha.app.net "App.net"
[APPDOTNETDEV]: https://account.app.net/developer/apps/ "App.net Developer Area"
[OVER9000]: http://www.youtube.com/watch?v=SQYakKz3i6E "It's Over 9000"
[IFTTT]: http://ifttt.com/ "If This Then That"
[TWITTER-BLOCKS-IFTTT]: http://techcrunch.com/2012/09/20/ifttt-is-the-latest-service-to-be-affected-by-twitters-api-constraints-will-remove-triggers/ "IFTTT removes Twitter triggers"
[PYTHON-TWITTER]: https://github.com/bear/python-twitter "Python-Twitter"
[PYTHON-APPDOTNET]: https://github.com/simondlr/Python-App.net-API-Wrapper "Python App.net API Wrapper"
[TWITTER-RSS]: http://donaldburr.com/2012/09/27/two-ways-to-work-around-ifttts-removal-of-twitter-triggers/ "Twitter RSS triggers"
[PYTHON]: http://www.python.org "Python"
[SIMPLEJSON]: https://github.com/simplejson/simplejson "SimpleJSON"
[TWITTER-RSS-DEPRECATED]: https://dev.twitter.com/docs/deprecations/spring-2012 "Twitter RSS deprecated"
[SCREEN]: http://www.gnu.org/software/screen/ "Screen"
[TMUX]: http://tmux.sourceforge.net "tmux"
[GHISSUES]: https://github.com/dburr/twitter_adn_mirror/issues "Github Issues"
[GHFORK]: https://help.github.com/articles/fork-a-repo "Fork"
[DBURR]: http://DonaldBurr.com/ "Donald Burr"
[OTAKU]: http://otakunopodcast.com/ "Otaku no Podcast"
[DBURRAPPS]: http://DonaldBurr.com/apps/ "Donald Burr's Apps"

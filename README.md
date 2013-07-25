# Twitter to App.net Crossposter
##### by Donald Burr <dburr@borg-cube.com>

**Note this readme is still a work in progress**

### Purpose

This script allows you to crosspost your [Twitter][TWITTER] posts ("tweets")
to the new up-and-coming social network/app platform [App.net][APPDOTNET].
It was created because I wanted a quick and simple way to share content
to both services (I simply don't have [over 9,000 hours in the day][OVER9000]
to manage all these social networks, nor do I have the patience to do so).

In the past this task could be easily accomplished using a nifty service
called [If This Then That (IFTTT)][IFTTT].  However recently Twitter has
[blocked IFTTT access][TWITTER_BLOCKS_IFTTT] to the Twitter API, which
meant this method would no longer work.

[ff][TWITTER-RSS]


### Prerequisites

In order to use this script, you will need to install the following
Python modules, as well as their prerequisites.  Consult their Github
pages for instructions on how to do so.

* [Python][PYTHON] (tested with 2.6.6 and 2.7.2)
* [Python-Twitter][PYTHON-TWITTER]
* [Python App.net API Wrapper][PYTHON-APPDOTNET]
* [SimpleJSON][SIMPLEJSON]

### Setup

Once those are installed, take a look at config.sample, copy it and
edit, then get your Twitter and App.net API keys.

### Future Plans

Some ideas for features/enhancements that I will try and implement.

* Option to crosspost @mentions if there is a user with the same name
  on App.net
* Mechanism to filter posts, that is, to prevent crossposting of posts
  that match certain criteria (regexp, client name, etc.)  This can be
  used to, e.g. not crosspost auto-posts from checkin services
  (e.g. Foursquare).

[TWITTER]: http://twitter.com "Twitter"
[TWITTERDEV]: https://dev.twitter.com "Twitter Developer"
[APPDOTNET]: https://alpha.app.net "App.net"
[APPDOTNETDEV]: https://account.app.net/developer/apps/ "App.net Developer Area"
[OVER9000]: http://www.youtube.com/watch?v=SQYakKz3i6E "It's Over 9000"
[IFTTT]: http://ifttt.com/ "If This Then That"
[TWITTER_BLOCKS_IFTTT]: http://techcrunch.com/2012/09/20/ifttt-is-the-latest-service-to-be-affected-by-twitters-api-constraints-will-remove-triggers/ "IFTTT removes Twitter triggers"
[PYTHON-TWITTER]: https://github.com/bear/python-twitter "Python-Twitter"
[PYTHON-APPDOTNET]: https://github.com/simondlr/Python-App.net-API-Wrapper "Python App.net API Wrapper"
[TWITTER-RSS]: http://donaldburr.com/2012/09/27/two-ways-to-work-around-ifttts-removal-of-twitter-triggers/ "Twitter RSS triggers"
[PYTHON]: http://www.python.org "Python"
[SIMPLEJSON]: https://github.com/simplejson/simplejson "SimpleJSON"

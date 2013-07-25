#!/usr/bin/python

"""
Usage: mirror [-c | --config=configuration file (default: `mirror.cfg')]
              [-i | --poll-interval=period in secs between polls (default=300)
              [-m | --mirror-mentions]
              [-d | --mirror-indirect-mentions]
              [-r | --mirror-retweets]
              [-u | --user-to-mirror=username to mirror]
              [-n | --simulation-mode]

Note: command-line arguments take precedence, followed by config files.
"""

# Twitter to App.net Crossposter
# Copyright (c) 2013 Donald Burr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import simplejson as json
import time
import datetime
import datetime
import twitter
import unicodedata
import re
import sys
import sched
import getopt
from ConfigParser import SafeConfigParser
from appdotnet import *

config_file = "mirror.cfg"
poll_interval = 300
last_run_time = time.time()
mirror_mentions = False
mirror_indirect_mentions = False
mirror_retweets = False
simulation_mode = False

twitter_api = None
app_net_api = None

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS_TOKEN_KEY = ''
TWITTER_ACCESS_TOKEN_SECRET = ''

# App.net Credentials
APP_NET_CLIENT_ID = ''
APP_NET_CLIENT_SECRET = ''
APP_NET_CALLBACK_URL = ''
APP_NET_ACCESS_TOKEN = ''
APP_NET_SCOPE = ['write_post']

user_to_mirror = None

s = sched.scheduler(time.time, time.sleep)

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

###############################################################################

def getSec(s):
  l = s.split(':')
  return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

###############################################################################

def getHMS(s):
  if not isinstance(s, float):
    if isinstance(s, str):
      s = getSec(s)
    else:
      s = float(s)
  hms = time.strftime('%H:%M:%S', time.gmtime(s))
  return hms

###############################################################################

def read_config(config_file):
  global TWITTER_CONSUMER_KEY
  global TWITTER_CONSUMER_SECRET
  global TWITTER_ACCESS_TOKEN_KEY
  global TWITTER_ACCESS_TOKEN_SECRET

  global APP_NET_CLIENT_ID
  global APP_NET_CLIENT_SECRET
  global APP_NET_CALLBACK_URL
  global APP_NET_ACCESS_TOKEN
  global APP_NET_SCOPE

  global user_to_mirror
  global mirror_mentions
  global mirror_indirect_mentions
  global mirror_retweets
  global poll_interval

  try:
    file_object = open(config_file, "r")
    parser = SafeConfigParser()
    parser.readfp(file_object)

    config = dict((section, dict((option, parser.get(section, option))
                                  for option in parser.options(section)))
                                  for section in parser.sections())

    twitter_credentials = config["twitter"]
    app_net_credentials = config["appdotnet"]
    other_prefs = config["other"]

    TWITTER_CONSUMER_KEY = twitter_credentials.get("consumer_key", "")
    TWITTER_CONSUMER_SECRET = twitter_credentials.get("consumer_secret", "")
    TWITTER_ACCESS_TOKEN_KEY = twitter_credentials.get("access_token_key", "")
    TWITTER_ACCESS_TOKEN_SECRET = twitter_credentials.get("access_token_secret", "")
    user_to_mirror = twitter_credentials.get("user_to_mirror", "")

    APP_NET_CLIENT_ID = app_net_credentials.get("client_id", "")
    APP_NET_CLIENT_SECRET = app_net_credentials.get("client_secret", "")
    APP_NET_CALLBACK_URL = app_net_credentials.get("callback_url", "")
    APP_NET_ACCESS_TOKEN = app_net_credentials.get("access_token", "")

    mirror_mentions = other_prefs.get("mirror_mentions", mirror_mentions)
    mirror_indirect_mentions = other_prefs.get("mirror_indirect_mentions", mirror_indirect_mentions)
    mirror_retweets = other_prefs.get("mirror_retweets", mirror_retweets)
    poll_interval = other_prefs.get("poll_interval", poll_interval)
    if isinstance(poll_interval, basestring):
      poll_interval = int(poll_interval)

  except IOError, (errno, strerror):
    print "I/O error(%s): %s: %s" % (errno, strerror, config_file)
    sys.exit(1)
  except KeyboardInterrupt:
    print "Exiting due to user interrupt."
    sys.exit(1)
  except:
    print "Unexpected error:", sys.exc_info()[0]
    sys.exit(1)

###############################################################################

def setup_api_connections():
  global twitter_api
  global app_net_api

  global TWITTER_CONSUMER_KEY
  global TWITTER_CONSUMER_SECRET
  global TWITTER_ACCESS_TOKEN_KEY
  global TWITTER_ACCESS_TOKEN_SECRET
  global user_to_mirror

  global APP_NET_CLIENT_ID
  global APP_NET_CLIENT_SECRET
  global APP_NET_CALLBACK_URL
  global APP_NET_ACCESS_TOKEN
  global APP_NET_SCOPE

  print "Setting up API connections..."

  # first let's do twitter
  # can't proceed without all of the twitter credentials

  if TWITTER_CONSUMER_KEY \
    and TWITTER_CONSUMER_SECRET \
    and TWITTER_ACCESS_TOKEN_KEY \
    and TWITTER_ACCESS_TOKEN_SECRET \
    and user_to_mirror:
    twitter_api = twitter.Api(
      consumer_key=TWITTER_CONSUMER_KEY,
      consumer_secret=TWITTER_CONSUMER_SECRET,
      access_token_key=TWITTER_ACCESS_TOKEN_KEY,
      access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    verification = twitter_api.VerifyCredentials()
    if verification:
      print "Twitter authentication was successful."
    else:
      print "Error: There was a problem authenticating with Twitter."
      print "Please check your credentials and try again."
      sys.exit(1)

  else:
    print "Error: missing one or more Twitter credentials."
    print "Please check config and try again."
    sys.exit(1)

  # Now let's do App.net
  # This is a bit trickier, there are two possible states
  # We NEED client_id, client_secret and callback_url

  if APP_NET_CLIENT_ID \
    and APP_NET_CLIENT_SECRET \
    and APP_NET_CALLBACK_URL:

    # now if there is a access_token, just use it to authenticate
    if not APP_NET_ACCESS_TOKEN:
      # we need to authenticate
      app_net_api = appdotnet(APP_NET_CLIENT_ID,APP_NET_CLIENT_SECRET,APP_NET_CALLBACK_URL,APP_NET_SCOPE)
      url = app_net_api.generateAuthUrl()
      print "App.net auth url: %s" % url
      print "Browse to that url, then paste the url you get redirected to here."
      redirect_string = raw_input(':')
      m = re.search('^.*code=(.+?)$', redirect_string)
      if m:
        found = m.group(1)
        response_json = app_net_api.getAuthResponse(found)
        response_object = json.loads(response_json)
        access_token = response_object["access_token"]
        print "Your access token is:"
        print access_token
        print "Save this value in your configuration file (or otherwise make a note"
        print "of it) and re-run this script."
        sys.exit(0)
      else:
        print "HEY, something is wrong, could not find the access code!"
        sys.exit(1)

    else:
      app_net_api = appdotnet(access_token=APP_NET_ACCESS_TOKEN)
      if app_net_api:
        print "App.net authentication successful."
      else:
        print "Unable to authenticate with App.net"
        sys.exit(1)

  else:
    print "Error: missing one or more App.net credentials."
    print "Please check config and try again."
    sys.exit(1)

def run(sc):
  global poll_interval
  global last_run_time
  global twitter_api
  global app_net_api
  global mirror_mentions
  global mirror_retweets
  global user_to_mirror
  global simulation_mode

  now = datetime.datetime.now()

  print "Starting run at %s" % now.strftime("%Y-%m-%d %H:%M")
  print "==============================================================================="
  print "Finding posts made by @%s since %s..." % (user_to_mirror, time.asctime(time.localtime(last_run_time)))

  statuses = twitter_api.GetUserTimeline(user_to_mirror)
  sorted_statuses = sorted(statuses, key=lambda status: status.created_at_in_seconds)
  for s in sorted_statuses:
    if s.created_at_in_seconds > last_run_time:
      #text = unicodedata.normalize('NFKD', s.text).encode('ascii','ignore')
      text = s.text
      #text = text.rstrip()
      print "  %s" % text
      is_mention = False
      is_indirect_mention = False
      is_retweet = False
      if "RT @" in text or "(via @" in text:
        print "  (Retweet detected)"
        is_retweet = True
      elif s.in_reply_to_screen_name:
        print "  (in reply to a post from @%s)" % s.in_reply_to_screen_name
        is_mention = True
      elif re.search('^@([A-Za-z0-9]+?)$', text):
        m = re.search('^@([A-Za-z0-9]+?)$', text)
        who_mentioned = m.group(1)
        print "  (@mention of @%s detected)" % who_mentioned
        is_mention = True
        continue
      elif re.search('@([A-Za-z0-9]+?)$', text):
        m = re.search('@([A-Za-z0-9]+?)$', text)
        who_mentioned = m.group(1)
        print "  (Indirect @mention of %s detected)" % who_mentioned
        is_indirect_mention = True
      # now check if we want to post it
      if is_mention and not mirror_mentions:
        print "  (Mirroring of mentions disabled)"
        continue
      if is_indirect_mention and not mirror_indirect_mentions:
        print "  (Mirroring of indirect mentions disabled)"
        continue
      if is_retweet and not mirror_retweets:
        print "  (Mirroring of retweets disabled)"
        continue
      # okay we want to post it
      if not simulation_mode:
        print "    Posting...",
        return_json = app_net_api.createPost(text)
        return_object = json.loads(return_json)
        code = return_object["meta"]["code"]
        if (code == 200):
          print "ok"
        else:
          print "post failed"
      else:
        print "  (Running in simulation mode; not posting)"

  last_run_time = time.time()
  next_run = datetime.datetime.now() + datetime.timedelta(seconds=poll_interval)
  print ''
  a = datetime.timedelta(seconds=poll_interval)
  print "Next run in %s (at %s)" % (str(a), next_run.strftime("%Y-%m-%d %H:%M"))

  sc.enter(poll_interval+2, 1, run, (sc,))

  for x in range(poll_interval): 
    y = poll_interval - x
    b = datetime.timedelta(seconds=y)
    print '\r%s '%str(b), 
    sys.stdout.flush() 
    time.sleep(1)  

  print '\r             '
  print ''
  print ''

###############################################################################

def main(argv=None):
  # set default poll interval here
  global poll_interval
  global mirror_mentions
  global mirror_indirect_mentions
  global mirror_retweets
  global config_file
  global simulation_mode

  override_poll_interval = None
  override_mirror_mentions = None
  override_mirror_indirect_mentions = None
  override_mirror_retweets = None

  if argv is None:
    argv = sys.argv
  # parse command line options
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hc:i:mrdn", ["help", "config=", "poll-interval=", "mirror-mentions", "mirror-indirect-mentions", "mirror-retweets", "simulation-mode"])
    except getopt.error, msg:
      raise Usage(msg)

    for o, a in opts:
      if o in ("-h", "--help"):
        print __doc__
        return 0
      elif o in ("-i", "--poll-interval"):
        override_poll_interval = int(a)
      elif o in ("-c", "--config"):
        config_file = a
      elif o in ("-m", "--mirror-mentions"):
        override_mirror_mentions = True
      elif o in ("-d", "--mirror-indirect-mentions"):
        override_mirror_indirect_mentions = True
      elif o in ("-r", "--mirror-retweets"):
        override_mirror_retweets = True
      elif o in ("-n", "--simulation-mode"):
        simulation_mode = True

    # read in config file
    read_config(config_file)

    # command line arguments override config file
    if override_poll_interval:
      poll_interval = override_poll_interval
    if override_mirror_mentions:
      mirror_mentions = override_mirror_mentions
    if override_mirror_indirect_mentions:
      mirror_indirect_mentions = override_mirror_indirect_mentions
    if override_mirror_retweets:
      mirror_retweets = override_mirror_retweets

    # set up the api connection
    setup_api_connections()
    print

    # main run loop
    s.enter(0, 1, run, (s,))
    s.run()

  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

###############################################################################

if __name__ == "__main__":
  sys.exit(main())

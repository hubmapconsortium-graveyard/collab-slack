# 

usage_string='channelMembers.py -t <slack-auth-token> -c <slack-channel-name> [--email|--id|--real_name]'

def usage():
  print usage_string
  sys.exit(2)
def help():
  print usage_string
  print "  -t|token      Retrieve slack auth token here: https://api.slack.com/custom-integrations/legacy-tokens"
  print "  -c|channel    Omit '#' from slack channel name; e.g., #userneeds becomes userneeds"
  sys.exit(2)


import sys, getopt
import json
import urllib2

def main(argv):
  opt_slack_token = ''
  opt_channel_nmae = ''
  opt_print_real_name = False
  opt_print_id = False
  opt_print_email = False
  try:
    opts, args = getopt.getopt(argv,"ht:c:rie",["token=","channel=","real_name","id","email"])
  except getopt.GetoptError:
    usage()
  for opt, arg in opts:
    if opt == '-h':
      help()
    elif opt in ("-t", "--token"):
      opt_slack_token = arg
    elif opt in ("-c", "--channel"):
      opt_channel_name = arg
    elif opt in ("-r", "--real_name"):
      opt_print_real_name = True
    elif opt in ("-i", "--id"):
      opt_print_id = True
    elif opt in ("-e", "--email"):
      opt_print_email = True

  if opt_slack_token == "" or opt_channel_name == "":
    print "Error: both slack-auth-token and slack-channel-name are required"
    usage()

  members = urllib2.urlopen('https://slack.com/api/users.list?token='+opt_slack_token+'&pretty=1')
  members_data = json.load(members)
  members_obj = members_data["members"]
  member_dict={}
  for member in members_obj:
    if not member["is_bot"] and member["name"] != "slackbot":
      member_dict[member["id"]] = ""
      # xxx doesn't account for order of input options
      if opt_print_id:
        member_dict[member["id"]] = member_dict[member["id"]] + member["id"]+"\t"
      if opt_print_real_name:
        member_dict[member["id"]] = member_dict[member["id"]] + member["profile"]["real_name"]+"\t"
      if opt_print_email:
        member_dict[member["id"]] = member_dict[member["id"]] + "<"+member["profile"]["email"]+">"+"\t"
  # xxx maybe strip the tab off after

  channels = urllib2.urlopen('https://slack.com/api/conversations.list?token='+opt_slack_token+'&pretty=1')
  channels_data = json.load(channels)
  channels_obj = channels_data["channels"]
  for channel in channels_obj:
    if channel["name"] == opt_channel_name:
      memberids = urllib2.urlopen('https://slack.com/api/channels.info?token='+opt_slack_token+'&channel='+channel["id"]+'&pretty=1')
      memberids_data = json.load(memberids)
      memberids_obj = memberids_data["channel"]["members"]
      for memberid in memberids_obj:
        print member_dict[memberid]


if __name__ == "__main__":
  main(sys.argv[1:])

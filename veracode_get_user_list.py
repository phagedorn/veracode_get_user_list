import sys
import requests
import argparse
import json
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import VeracodeAPI as vapi
headers = {"User-Agent": "Python HMAC Example"}

def main():

# test comment
    parser = argparse.ArgumentParser(
        description='This script takes a user name and generates a list of their attributes or --all will generate a list of all users and attributes.')
    parser.add_argument('-u', '--user', help='print attributes for this user',required=False)
    parser.add_argument('--all',default=False, action='store_true', help='If set to True information for all users will be generated', required=False)
    parser.add_argument('--file',default=False, action='store_true', help='If set to True information will be placed in a file called user_list.csv', required=False) 
    parser.add_argument('-t','--team', default=False, action='store_true', help='If set to True it will output the default team information', required=False)
    parser.add_argument('-tid', '--teamid', help='print memvers of this team',required=False)
    parser.add_argument('-c', '--channel', help='print attributes for this user',required=False)
    args = parser.parse_args()
    file_name = "user_list.csv"

    if (args.file):
        # delete old files
        f = open(file_name, 'w')
        print("user name, ip restricted, allowed ip addresses", file=f)
    if (args.user is not None):
       data = vapi().get_user_by_search(args.user)
       for user in data:
          userguid = user["user_id"]
          data2 = vapi().get_user(userguid)
          if (str(data2["ip_restricted"]) == "True"):
             usr_str = user["user_name"]+","+str(data2["ip_restricted"])+","+str(data2["allowed_ip_addresses"])
          else:
             usr_str = user["user_name"]+","+str(data2["ip_restricted"])
          if (args.file):
             print(usr_str, file=f)
          else:
             print(usr_str)
    elif (args.all):
       data = vapi().get_users()
       for user in data:
          if ( str(user["saml_user"]) == "True"):
            userguid = user["user_id"]
            data2 = vapi().get_user(userguid)
            if (str(data2["ip_restricted"]) == "True"):
               usr_str = user["user_name"]+","+str(data2["ip_restricted"])+","+str(data2["allowed_ip_addresses"])
            else:
               usr_str = user["user_name"]+","+str(data2["ip_restricted"])
            if (args.file):
               print(usr_str, file=f)
            else:
               print(usr_str)
    elif(args.teamid):
       teamid = args.teamid
       team = vapi().get_team_by_id(teamid)
       channel = args.channel 
       dict = {}
       for user in team['users']:
         user_name = user['user_name'].split("-")
         email = user_name[0]
         dict1 = {user['last_name']:email}
         dict.update(dict1)
       count_members = len(dict)
       dict1 = {"count":count_members}
       dict.update(dict1)
       payload = {"text": str(dict)}
       if ( count_members == 0 ):
         print("No new members in group: default")
       else:
         print("Send message to MS Teams with new members")
         print(dict)
         headers = {'Content-Type': 'application/json'}
         response = requests.post(channel, headers=headers, data=json.dumps(payload))
         print(response.text.encode('utf8'))


    else:
       print ('You must specify either --all or a user with -u, --user, --team with teamid=YOUR_TEAM_ID')
    exit(0)

if __name__ == '__main__':
    main()

#!/usr/bin/python3.7

import pandas as pd 
#python -m pip install pandas ///for installation
from bs4 import BeautifulSoup
#python -m pip install BeautifulSoup4 ///for installation
import requests
#python -m pip install requests ///for installation
import csv
import json
import os

                                                            #MERGE INITIAL TWO FILES
a = pd.read_csv("C://FileA.csv")
b = pd.read_csv("C://FileB.csv")
merged = a.merge(b, on='user_id')


                                                            #READ API INTO CSV FOR MERGE
url = "https://sandbox.tinypass.com/api/v3/publisher/user/list?aid=o1sRRZSLlw&api_token=zziNT81wShznajW2BD5eLA4VCkmNJ88Guye7Sw4D"
html_content = requests.get(url).text
response2 = BeautifulSoup(html_content, "lxml")
response = response2.body.text
response3 = json.loads(response)
users_parsed = json.loads(response)                         #read URL
usr_data = users_parsed["users"]
user_data = open('C://API_users.csv', 'w')
csvwriter = csv.writer(user_data)
count = 0
for usr in usr_data:
      if count == 0:
             header = usr.keys()
             csvwriter.writerow(header)
             count += 1
      csvwriter.writerow(usr.values())
user_data.close()

                                                           #MERGE FileA,FileB,API_users
c = pd.read_csv("C://API_users.csv")
c.columns = ["first_name","last_name","personal_name","email","user_id","image1","create_date","reset_password_email_sent","custom_fields"]
c2 = c [["user_id","email","first_name","last_name"]]
left_merged = merged.merge(c2, how="left", on="email")
left_merged.rename(columns={'first_name_x':'first_name','last_name_x':'last_name','user_id_y':'user_id'},inplace=True)
left_merged.user_id.fillna(left_merged.user_id_x, inplace=True)
left_merged2 = left_merged[["email","first_name","last_name","user_id"]]
#os.remove("C://API_users.csv")                            #API USERS LIST FILE REMOVAL IN CASE IF RELEVANT
left_merged2.to_csv("C://output.csv", index=False)         #FINAL MERGED FILE to CSV C://output.csv

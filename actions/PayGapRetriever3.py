# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:15:45 2021

@author: david romero

Test file to load gender pay gap data from various EU and N.Am. countries
and display the info.
"""
#import pandas as pd
import datetime as dt
import csv

#ctry_name = 'Canada'
#df = pd.read_csv("gpg_intl.csv", delimiter=',')
#df = df[df['country'] == ctry_name]
#gpg = df.iat[0,1]      
#print("{}{}{}{}{}".format("The avg. gender pay gap in ", ctry_name, " is ", gpg, "%"))

def get_the_time():
    #current_time = f"{dt.datetime.now()}"
    current_time =  dt.datetime.now()
    time_str = "It's " + current_time.strftime("%I:%M %p")
    #print(current_time.strftime("%A, %I:%M %p"))
    return (time_str)

def get_gpg_intl(ctry_name):
    gpg_file = 'gpg_intl.csv'
    gpg_dict = {}
    with open(gpg_file) as data:
        reader = csv.reader(data)
        header_row = next(reader)
        for row in reader:
            key = row[0]
            gpg_val = row[1]
            gpg_dict[key] = gpg_val

    report_yr = '2019'
    gpg_result = gpg_dict[ctry_name]
    reply = "{}{}{}{}{}{}{}".format("The avg. gender pay gap in ", report_yr, " in ", ctry_name, " was ", gpg_result, "%")
    #print(reply)
    return(reply)

def get_gpg_uk(company):
    gpg_file = 'gpg_uk.csv'
    gpg_dict = {}
    with open(gpg_file) as data:
        reader = csv.reader(data)
        header_row = next(reader)
        for row in reader:
            key = row[0]
            gpg_val = row[1]
            gpg_dict[key] = gpg_val

    report_yr = '2020'
    gpg_result = gpg_dict[company]
    reply = "{}{}{}{}{}{}{}".format("The avg. gender pay gap in ", report_yr, " at ", company, " was ", gpg_result, "%")
    return(reply)


if __name__ == '__main__':
    print("GPG for a country:")
    print(get_gpg_intl('USA'))
    print("GPG for a UK Company:")
    print(get_gpg_uk('Google'))
    print(get_the_time())

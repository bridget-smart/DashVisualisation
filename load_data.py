"""
Preamble for most code and jupyter notebooks
@author: bridgetsmart
@notebook date: 15 Mar 2023
"""

import numpy as np, pandas as pd
import math, string, re, pickle, json, time, os, sys, datetime, itertools


def politics_AU_cmap():
    # colours from 
    # https://coolors.co/f51f17-9c089c-0eb7b7-093879-0797ff-6be3ff-51d224-ff8200-ffd800

    # checked colourblind
    # https://davidmathlogic.com/colorblind/#%23F51F17-%239C089C-%230EB7B7-%23093879-%230797FF-%236BE3FF-%2351D224-%23FF8200-%23FFD800

    cmap = {'Labor': (251/255, 9/255, 0/255), # red
            'Katter\'s Australian': (156/255, 8/255, 156/255), # purple
            'Teal Independent': (14/255, 183/255, 183/255), # teal
            'National': (9/255, 56/255, 121/255), # dark blue
            'Liberal': (7/255, 151/255, 244/255), # mid blue
            'Liberal National': (107/255, 227/255, 255/255), # yellow
            'Greens': (81/255, 210/255, 36/255), # green
            'Centre Alliance': (255/255, 130/255, 0), # orange
            'Independent': (255/255, 216/255, 0/255)} # pink

    return cmap

def load_data(selection = None, liwc_logical = False):

    if not selection:
        a=True
        
        while a:
            a=False
            try:
                selection = int(input('Which data do you want loaded? \n(1) All tweets, \n(2) politician tweets, \n(3) News tweets, \n(4) HoR Following, \n(5) HoR User details, or\n(6) Account classifications? Input 7 to cancel.'))
                if selection>7:
                    print('Selection invalid, try again.')
                    a=True
                if selection<1:
                    print('Selection invalid, try again.')
                    a=True
            except:
                print('Please input a number.')

        # Load in LIWC logical conditional
        if selection < 4:
            liwc_logical = False
            sa = input('Do you want to load LIWC tags? These can use a substantial amount of memory so be careful. (Y/N)?')
            if sa == 'Y':
                print('Note this will increase the loading time and memory requirement.')
                liwc_logical = True

    if selection==1:
        print('Expect to wait around 7-8 minutes...')
        with open('AUNewsPoliticsDatasetTwitter/HoRNewsAUTweets.pkl','rb') as f:
            all_tweets = pickle.load(f)

        all_tweets.created_at = all_tweets.created_at.map(pd.to_datetime)

        if liwc_logical:
            all_tweets = load_liwc(liwc_logical, all_tweets)

        return all_tweets
    
    if selection ==2:
        print('Expect to wait around 6-7 minutes...')
        with open('AUNewsPoliticsDatasetTwitter/HoRAUTweets.pkl','rb') as f:
            politician_tweets = pickle.load(f)

        politician_tweets.created_at = politician_tweets.created_at.map(pd.to_datetime)

        if liwc_logical:
            politician_tweets = load_liwc(liwc_logical, politician_tweets)

        return politician_tweets
    
    if selection==3:
        with open('AUNewsPoliticsDatasetTwitter/NewsAUTweets.pkl','rb') as f:
            news_tweets = pickle.load(f)

        news_tweets.created_at = news_tweets.created_at.map(pd.to_datetime)

        if liwc_logical:
            news_tweets = load_liwc(liwc_logical, news_tweets)
        
        return news_tweets
    
    if selection==4:
        # 2022 HoR Following
        with open('AUNewsPoliticsDatasetTwitter/HoR2022Following.pkl', 'rb') as f:
            HoR2022Following = pickle.load(f)
        return HoR2022Following
    
    if selection==5:
        # 2022 HoR Following
        HoR_users = pd.read_csv('AUNewsPoliticsDatasetTwitter/UsersHoR.txt', index_col=0)
        return HoR_users
    
    if selection==6:
        return pd.read_csv('AUNewsPoliticsDatasetTwitter/account_classifications.csv', index_col=0)
    
    if selection==7:
        print('Exiting...')
        return 0
    
    print('Selection invalid, try again.')
    return False


def load_liwc(liwc_logical, df):
    if liwc_logical:
        # load in LIWC
        with open('AUNewsPoliticsDatasetTwitter/LIWC/tweets_liwc.pkl','rb') as f:
            liwc_all = pickle.load(f)

        # more efficient
        liwc_filtered = {k:liwc_all[k] for k in set(df.id)}
        liwc_scores = pd.DataFrame(liwc_filtered).transpose()

        # join to original df
        df = df.join(liwc_scores, on='id')
        return df

    return df
    # join to df

        
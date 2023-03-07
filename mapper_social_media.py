#! /home/bigdata/anaconda3/bin/python3

import sys
import simplejson as json
from datetime import datetime

month_dict = dict({
    "Jan": "01", "Feb": "02", "Mar": "03",
    "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09",
    "Oct": "10", "Nov": "11", "Dec": "12"
})

for line in sys.stdin:
    try:
        # parse the incoming json
        posts = json.loads(line.strip())

    except Exception as e:
        sys.stderr.write("unable to parse json, expected single line: %s" % e)
        continue
    
    #if youtube
    if "snippet" in posts[0]: 
        for post in posts:
            try:
                # format yyyy-mm-dd
                post_date = post["snippet"]["publishedAt"].split('T')[0]
                print("youtube\t%s" % post_date)
            
            except Exception as e:
                sys.stderr.write("certain attribute doesn't exist: %s" % e)
                continue

    # if facebook
    elif "crawler_target" in posts[0] and posts[0]["crawler_target"]["specific_resource_type"] == "facebook":
        for post in posts:
            try:
                post_date = post["created_time"].split('T')[0]
                print("%s" % post_date)

                if "comments" in post:
                    if "data" in post["comments"]:
                        for comment in post["comments"]["data"]:
                            try:
                                comment_date = comment["created_time"].split('T')[0]
                                print("facebook\t%s" % comment_date)
                            
                            except Exception as e:
                                sys.stderr.write("certain attribute doesn't exist: %s" % e)
                                continue
                
                else:
                    continue
            

            except Exception as e:
                sys.stderr.write("certain attribute doesn't exist: %s" % e)
                continue
    
    #if IG
    elif "object" in posts[0] and posts[0]["object"]["social_media"] == "instagram":
        for post in posts:
            try:
                # format yyyy-mm-dd
                try:
                    post_timestamp = int(post["created_time"])
                    post_date = str(datetime.utcfromtimestamp(post_timestamp).strftime('%Y-%m-%d'))
                
                except Exception as e:
                    sys.stderr.write("failed converting from timestamp: %s" % e)
                    continue                
                
                print("instagram\t%s" % post_date.split(' ')[0])

                
            except Exception as e:
                sys.stderr.write("certain attribute doesn't exist: %s" % e)
                continue
    
    # if twitter
    elif "retweeted" in posts[0]:
        for post in posts:
            try:
                # format yyyy-mm-dd
                try:
                    post_dayname, post_month, post_daydate, post_ts, post_offset, post_year = post["created_at"].split(' ')
                    post_month = month_dict[post_month]

                except Exception as e:
                    sys.stderr.write("failed while converting: %s" % e)
                    continue

                print("twitter\t%s-%s-%s" % (post_year, post_month, post_daydate))
            
            except Exception as e:
                sys.stderr.write("certain attribute doesn't exist: %s" % e)
                continue
    
    else:
        continue


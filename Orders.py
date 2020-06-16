# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:48:33 2020

@author: mdevasish
"""

import pandas as pd
from datetime import timedelta
from collections import Counter
import json

data = pd.read_csv('order_brush_order.csv',parse_dates = [3])
data = data.sort_values(by = 'event_time')

shops = set(data['shopid'])

req_dict = dict()

#with open('req_dict.json','w') as f:
#    json.dump(req_dict,f)

# Looping for each shopid
for each in shops:
    #print(each)
    
    df = data[data['shopid']==each]
    final = []
    
    # Gathering shopids with more than 3 transactions
    if df.shape[0] >= 3:
        user_id = []
        
        # Create a window and slide it over the start to end of timeline of transactions
        for i in range(len(df)):
            
            start = df['event_time'].iloc[i]
            end = start + timedelta(hours = 1)
            req = df[(df['event_time'] >= start) & (df['event_time'] <= end)]
            metric = req.shape[0]/len(set(req['userid']))
            
            if metric >= 3:
                count = dict(Counter(req['userid']))
                #max_count = max([value/len(count) for value in count.values()])
                max_count = max([value for value in count.values()])
                for key,value in count.items():
                    if value == max_count:
                        user_id.append(key)
                        #user_id = list(set(user_id))
            final.extend(user_id)
            final = list(set(final))
        #final.extend(user_id)
        req_dict [each] = final
    else:
        req_dict [each] = []
        

new = {k:v for k,v in sorted(req_dict.items(),key = lambda item: item[1],reverse = True)}
frame = pd.DataFrame.from_dict(new,orient = 'index')
frame = frame.fillna(0)
frame.columns = ['col1','col2','col3','col4']
frame.to_csv('submit.csv')


#with open('req_dict.json','w') as f:
#    json.dump(req_dict,f)   
        
    
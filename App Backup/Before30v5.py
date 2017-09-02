#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 15:02:09 2017

@author: anand
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 13:27:40 2017

@author: anand
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 12:15:50 2017

@author: anand
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure, show
import collections
import os
from bokeh.io import curdoc
from bokeh.models import Select, DatetimeTickFormatter, ColumnDataSource, BoxSelectTool,LassoSelectTool
from bokeh.layouts import widgetbox, row, gridplot, layout

dir1 = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(dir1,'url.csv'),sep=",")
df = df.fillna(0)
goals = df.columns.values.tolist()


#%%
goals_dict = {'Adventure Sports':[],'Florida':[],'Go Slutty':[],'Colour Hair':[],'Fountain Spa':[],'Road Trip':[]}

[goals_dict[key].append(df[key]) for key in goals_dict]            

#%%
TOOLS="pan,wheel_zoom,reset,hover,box_select,lasso_select"

def create_source(g):
    data_dict = {}
    for i in xrange(len(goals_dict[g][0])):
        data_dict['url'+'%s'%i] = [goals_dict[g][0][i]]
# =============================================================================
#         if (goals_dict[g][0][i]!= 0):
#             data_dict['url'+'%s'%i] = [goals_dict[g][0][i]]
#         else:
#             continue
# =============================================================================
    data_dict = collections.OrderedDict(sorted(data_dict.items()))
    return (ColumnDataSource(data_dict))
        
    

def create_plot(source):    
    img_set = []
    dff = source.to_df()
    for i in xrange(dff.shape[1]):
        p = figure(tools=TOOLS,plot_height=400,plot_width=400,x_range=(0,10), y_range=(0,10))
        p.image_url(url=dff.columns[i],x=5,y=5,w=10,h=10,anchor='center',source=source)
        p.axis.visible=False
        img_set.append(p)        
    return img_set   
    
    
def function_to_call(attr, old, new): 
    goal = select.value
    src = create_source(goal)
    source.data.update(src.data)
    print(goal)


#%%
goal = goals[0]
select = Select(options=goals, value=goal, title="Before 30")

source = create_source(goal)

select.on_change('value', function_to_call)
plot = create_plot(source)


#%%

final = []
count = 0
while (count<len(plot)): 
    temp = []
    while(len(temp)<2):
        temp.append(plot[count])
        count += 1
        if (count==len(plot)):
            final.append(temp)
            break
    if (count==len(plot)):
        break
    final.append(temp)
    
#%%
grid = gridplot(final)
layout = layout([
        [widgetbox(select)],
        [grid]])
curdoc().add_root(layout)


# =============================================================================
# lt = row(grid,widgetbox(select))
# show(lt)
# =============================================================================



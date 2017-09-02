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
import os
from bokeh.io import curdoc
from bokeh.models import Select, DatetimeTickFormatter, ColumnDataSource, BoxSelectTool,LassoSelectTool
from bokeh.layouts import widgetbox, row, gridplot, layout

dir1 = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(dir1,'url.csv'),sep=",")
goals = df.columns.values.tolist()


#%%
goals_dict = {'Adventure Sports':[],'Florida':[],'Go Slutty':[],'Colour Hair':[],'Fountain Spa':[],'Road Trip':[]}

[goals_dict[key].append(df[key]) for key in goals_dict]            

#%%
TOOLS="pan,wheel_zoom,reset,hover,box_select,lasso_select"

def create_source(g):
    return (ColumnDataSource(dict(url1 = [goals_dict[g][0][0]],
                                  url2 = [goals_dict[g][0][1]],
                                  url3 = [goals_dict[g][0][2]],
                                  url4 = [goals_dict[g][0][3]]))) 
    

def create_plot(source):
    p1 = figure(tools=TOOLS,plot_height=400,plot_width=400,x_range=(0,10), y_range=(0,10)) 
    p1.image_url(url='url1',x=5,y=5,w=10,h=10,anchor='center',source=source)
    p1.axis.visible = False    

    
    p2 = figure(tools=TOOLS,plot_height=400,plot_width=400,x_range=(0,10), y_range=(0,10)) 
    p2.image_url(url='url2',x=5,y=5,w=10,h=10,anchor='center',source=source)
    p2.axis.visible = False
    
    p3 = figure(tools=TOOLS,plot_height=400,plot_width=400,x_range=(0,10), y_range=(0,10)) 
    p3.image_url(url='url3',x=5,y=5,w=10,h=10,anchor='center',source=source)
    p3.axis.visible = False
    
    p4 = figure(tools=TOOLS,plot_height=400,plot_width=400,x_range=(0,10), y_range=(0,10)) 
    p4.image_url(url='url4',x=5,y=5,w=10,h=10,anchor='center',source=source)
    p4.axis.visible = False

 
    
    grid = gridplot([[p1,p2],[p3,p4]])
    return(grid)
    
# =============================================================================
#     img_set = []
#     for i in xrange(source.to_df().shape[0]):
#         p = figure(tools=TOOLS,plot_height=400,plot_width=400,x_range=(0,10), y_range=(0,10))
#         p.image_url(url=[source.to_df().values[0][i]],x=5,y=5,w=10,h=10,anchor='center',source=source)
#         img_set.append(p)        
#     return img_set   
# =============================================================================
    
    
def function_to_call(attr, old, new): 
    goal = select.value
    src = create_source(goal)
    source.data.update(src.data)
    print(goal)


#%%
# =============================================================================
# goals = []
# 
# for k in goals_dict:
#     goals.append(k)
# =============================================================================

goal = goals[0]
select = Select(options=goals, value=goal, title="Before 30")

source = create_source(goal)

select.on_change('value', function_to_call)
plot = create_plot(source)


#%%
#grid = gridplot([[plot[0],plot[1]],[plot[3],plot[2]]])
layout = layout([
        [widgetbox(select)],
        [plot]])#row(plot,widgetbox(select))
#show(layout)
curdoc().add_root(layout)

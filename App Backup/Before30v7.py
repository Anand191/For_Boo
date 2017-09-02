#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 16:10:57 2017

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
from bokeh.models import Select, DatetimeTickFormatter, ColumnDataSource, BoxSelectTool,LassoSelectTool,TextInput
from bokeh.layouts import widgetbox, row, gridplot, layout
from sqlalchemy import create_engine, MetaData, Table, update, insert, delete
from sqlalchemy.orm import sessionmaker,load_only
from sqlalchemy.ext.declarative import declarative_base

#%%
dir1 = os.path.dirname(__file__)
db_file = os.path.join(dir1,'cdb.db')

engine = create_engine('sqlite:///{}'.format(db_file),echo=False)
Base = declarative_base(engine)

meta = MetaData(engine)
db = Table('cdb1', meta, autoload=True)
    
Session = sessionmaker(bind=engine)
session = Session()

#%%
df = pd.read_sql_table('cdb1',con=engine)  #pd.read_csv(os.path.join(dir1,'url.csv'),sep=",")
names = []
for i in xrange(len(df.columns)):
    names.append(df.columns[i].replace('_',' '))
    
df.columns = names
df = df.drop('id',axis=1)
#df = df.fillna(0)

goals = df.columns.values.tolist()

goals_dict = {'Adventure Sports':[],'Florida':[],'Go Slutty':[],'Colour Hair':[],
              'Fountain Spa':[],'Road Trip':[],'Trans Siberian':[]}

[goals_dict[key].append(df[key]) for key in goals_dict]            

#%%
TOOLS="pan,wheel_zoom,reset,hover,box_select,lasso_select"

def create_source(g):
    data_dict = {}
    for i in xrange(len(goals_dict[g][0])):
        data_dict['url'+'%s'%i] = [goals_dict[g][0][i]]
    data_dict = collections.OrderedDict(sorted(data_dict.items()))
    return (ColumnDataSource(data_dict))


def update_db(link):
    col = select.value
    col = col.encode('ascii','ignore')
    col = col.replace(' ','_')
# =============================================================================
#     d = delete(db).where(db.c[col]==None)
#     session.execute(d)
# =============================================================================
    id_val = session.query(db.c.id).all()[-1][0] + 1
    col_data = session.query(db.c[col]).all()
    arr = np.asarray(col_data)
    if(np.any(arr==None)):
        i = update(db).where(db.c.id==session.query(db).filter(db.c[col]==None).first()[0])
        i = i.values({col:link})
    else:
        i = insert(db)
        i = i.values({'id':id_val, col:link})
    session.execute(i)    
    print (col)      
    

def create_plot(source):    
    img_set = []
    dff = source.to_df()
    for i in xrange(dff.shape[1]):
         p = figure(tools=TOOLS,plot_height=400,plot_width=400,x_range=(0,10), y_range=(0,10))
         p.image_url(url=dff.columns[i],x=5,y=5,w=10,h=10,anchor='center',source=source)
         p.axis.visible=False
         img_set.append(p)
         
    return (img_set)
    
def function_to_call(attr, old, new): 
    goal = select.value
    src = create_source(goal)
    source.data.update(src.data)
    print(goal)
    
def my_text_input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)
    update_db(new)
    session.commit()
    
def callback(attr,old,new):
    fig = fig_select.value
    page = select.value
    page = page.replace(' ','_')
    j = update(db).where(db.c[page]==figures[fig][0])
    j = j.values({page:None})
    session.execute(j)
    session.commit()
    print(page)
    print('{} is being deleted'.format(fig))
    


#%%
goal = goals[0]
source = create_source(goal)

select = Select(options=goals, value=goal, title="Before 30")

figures = source.data
Fig = []
[Fig.append(k) for k in figures]
Fig = sorted(Fig)
Fig.append("--")
fig_select = Select(title="Delete Images", value=Fig[-1],options=Fig)

text_input = TextInput(value="", title="Add Image URL:")
text_input.on_change("value", my_text_input_handler)

fig_select.on_change('value',callback)
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
        [widgetbox(select), widgetbox(text_input)],
        [row(grid,widgetbox(fig_select))]])
curdoc().add_root(layout)





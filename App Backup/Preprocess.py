#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 17:10:09 2017

@author: anand
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 16:06:12 2017

@author: anand
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 12:25:22 2017

@author: anand
"""

#%%
import pandas as pd
import numpy as np
from datetime import datetime
import os

from time import time
from sqlalchemy import Column, Integer, Float, Date, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(dir,'url1.csv'),sep=",")

#%%Create db
Base = declarative_base()

class cdb1(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'cdb1'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer,primary_key=True, nullable=False) 
    Adventure_Sports = Column(String(250))
    Florida = Column(String(250))
    Go_Slutty = Column(String(250))
    Colour_Hair = Column(String(250))
    Fountain_Spa = Column(String(250))
    Road_Trip = Column(String(250))
    Trans_Siberian = Column(String(250))
    

engine = create_engine('sqlite:///cdb.db')
Base.metadata.create_all(engine)

df.to_sql(con=engine, index_label='id', name=cdb1.__tablename__, if_exists='replace')
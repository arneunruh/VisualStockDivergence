import pandas as pd
import os as os
from datetime import datetime, timedelta
import json as json
from pandas.io.data import *
import random


def download(_symbol,_file,_location = "./"):

    _symbol = _symbol.lower()

    if(len(_location) > 3):
        if(_location.endswith("/")) == False:
            _location = _location + "/"
    
    if(os.path.exists(_location+_file)):
        
        try:
            print "File exists"
            data1 = pd.read_hdf(_location+_file,_symbol)
            #print data1
            #print len(data1)
            
            last = data1.index[-1].to_datetime() + timedelta(days=1)
            current = datetime.today()
    
            if (last.date() <  current.date()):
                print "Update data"
                data2 = DataReader (_symbol, 'yahoo', last)
                #print data2
                bigdata=data1.append(data2,ignore_index = False)
                #print bigdata
                bigdata.to_hdf(_location+_file,_symbol,mode='w',format='table')
        except:
            pass
    
    else: 
        
        ohlcvac = None
        
        try:
            ohlcvac = DataReader (_symbol, 'yahoo', start ='01/01/2013')
        except:
            pass               
        
        if ohlcvac is None:
            print('Yahoo could not connect')
        else:
            print "Yahoo could connect"
            print "File created"
            createFile(_symbol,_file,_location,ohlcvac)
        

def createFile(_symbol,_file,_location,ohlcvac):
    if len(ohlcvac.index) > 252:
        h5file = pd.HDFStore(_location+_file); 
        h5file[_symbol]= ohlcvac; 
        h5file.close()

def toDataFrame(_location,_file,_symbol):
    
    df = None
    print _location+_file
    if(os.path.exists(_location+_file)):
        try:
            print "File found - build output"
            df = pd.read_hdf(_location+_file,_symbol)
        except:
            pass
    return df
    
        
def toJson(_location,_file,_symbol):
    
    print _location+_file
    if(os.path.exists(_location+_file)):
        try:
            print "File found - run logic "
            df = pd.read_hdf(_location+_file,_symbol)
            #no json output
            dict = {}
            records = []
            for index, row in df.iterrows():
                _date = str(index.date())
                _close = str(row['Adj Close'])
                _obv = str(row['Adj Close'] * random.randint(1,11)*0.5)
                _div = str(row['Adj Close'] * -0.5)
                #print _date, _close, _volume
                record = {"Date":_date, "Close":_close, "Obv":_obv,"Div":_div}
                #print record
                records.append(record)

                dict['stock']=records
                #print dict
            return json.dumps(dict) 
        except:
            pass
    else:
        return None
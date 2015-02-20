from pandas import *
from math import *
from pandas.io.data import DataReader
import statsmodels.api as sm
import datetime 
import matplotlib.pyplot as plt


#Average True Range
def ATR(df, n):
    i = 0
    TR_l = [0]
    while i < len(df.index)-1:
        TR = max(df["High"][i], df['Close'][i]) - min(df["Low"][i], df["Close"][i])
        TR_l.append(TR)
        i = i + 1
    TR_s = Series(TR_l)
    
    ATR = Series(ewma(TR_s, span = n, min_periods = n-1), name = 'ATR_' + str(n))
    
    return ATR

#Exponential Moving Average for adjusted close
def EMAAdjClose(df, n):
    EMA = Series(ewma(df['Adj Close'], span = n, min_periods = n - 1), name = 'EMAClose_' + str(n))
    df = df.join(EMA)
    return df

#Exponential Moving Average for on balance volume
def EMAObv(df, n):
    EMA = Series(ewma(df['Obv'], span = n, min_periods = n - 1), name = 'EMAObv_' + str(n))
    df = df.join(EMA) 
    return df

#Exponential Moving Average for divergence indicator
def EMADiv(df, n):
    EMA = Series(ewma(df['Div'], span = n, min_periods = n - 1), name = 'EMADiv_' + str(n))
    df = df.join(EMA) 
    return df

#On-balance Volume
def OBVFilter(df,k,l):
    i = 0
    OBV = [0]
    '''
        local Middle=(high[period-1]+low[period-1])/2;
        local D=(high[period-1]-low[period-1])/K;
        local Up=Middle+D;
        local Dn=Middle-D;

        local tmp;

        if close[period] > close[period - 1] and close[period] > Up then
            tmp = V[period - 1] + volume[period];
        elseif close[period] < close[period - 1] and close[period] < Dn then
            tmp = V[period - 1] - volume[period];
        else
            tmp = V[period - 1];
        end
    '''
    while i < len(df.index)-1:
        if(i == 0): 
            OBV.append(0)
        else:
            middle = (df['High'][i] + df['Low'][i])/2
            d = (df['High'][i] - df['Low'][i])/k 
            up = middle + d
            down = middle - d

            if df['Close'][i] > df['Close'][i-1] and df['Close'][i] > up:
                OBV.append(OBV[i]+df['Volume'][i])
                # print "up"
            elif df['Close'][i] < df['Close'][i-1] and df['Close'][i] < down:
                OBV.append(OBV[i]-df['Volume'][i])
                # print "down"
            else:
                OBV.append(OBV[i])
                # print "side"
        i = i + 1
        
    OBV = Series(OBV,index=df.index, name = 'Obv_' + str(l))
    df = df.join(OBV)
    return df

def GUPPYClose(df):
    df = EMAAdjClose(df,3)
    df = EMAAdjClose(df,5)
    df = EMAAdjClose(df,8)
    df = EMAAdjClose(df,11)
    df = EMAAdjClose(df,14)
    df = EMAAdjClose(df,17)
    df = EMAAdjClose(df,27)
    df = EMAAdjClose(df,32) 
    df = EMAAdjClose(df,37) 
    df = EMAAdjClose(df,42) 
    df = EMAAdjClose(df,47)
    df = EMAAdjClose(df,52)
    return df

def GUPPYObv(df):
    df = EMAObv(df,3)
    df = EMAObv(df,5)
    df = EMAObv(df,8)
    df = EMAObv(df,11)
    df = EMAObv(df,14)
    df = EMAObv(df,17)
    df = EMAObv(df,27)
    df = EMAObv(df,32) 
    df = EMAObv(df,37) 
    df = EMAObv(df,42) 
    df = EMAObv(df,47)
    df = EMAObv(df,52)
    return df

def GUPPYDiv(df):
    df = EMADiv(df,3)
    df = EMADiv(df,5)
    df = EMADiv(df,8)
    df = EMADiv(df,11)
    df = EMADiv(df,14)
    df = EMADiv(df,17)
    df = EMADiv(df,27)
    df = EMADiv(df,32) 
    df = EMADiv(df,37) 
    df = EMADiv(df,42) 
    df = EMADiv(df,47)
    df = EMADiv(df,52)
    return df

def HistVol(df):
    logreturns = np.log(df.Close / df.Close.shift(1))
    return (np.sqrt(252*logreturns.var()))

def normDf(df):
    df = (df - df.mean()) / (df.max() - df.min()) 
    return df

def buildClose(df):
   
    close = df['Adj Close']
    close = Series(close,index=close.index, name = 'Close') 
    close = pandas.DataFrame(close)
    close["Reg"] = sm.OLS(close["Close"],sm.add_constant(range(len(close.index)),prepend=True)).fit().fittedvalues 
    
    return close
        

def buildDiv(df):
    df = GUPPYClose(df) 
    div =   df.EMAClose_3 - df.EMAClose_5 + \
            df.EMAClose_8 - df.EMAClose_11 + \
            df.EMAClose_14 - df.EMAClose_17 + \
            df.EMAClose_27 - df.EMAClose_32 + \
            df.EMAClose_37 - df.EMAClose_42 + \
            df.EMAClose_47 - df.EMAClose_52 
    div = Series(div,index=div.index, name = 'Div') 
    div = pandas.DataFrame(div)
    div["Line"] = 0.0 
    print div.tail(5)
    return div

def buildObv(df):
    df = OBVFilter(df, 1.7, 1)
    df = OBVFilter(df, 3.4, 2)
    df = OBVFilter(df, 6.8, 3)
    obv = (df.Obv_1 + df.Obv_2 + df.Obv_3) / 3
    obv = Series(obv,index=obv.index, name = 'Obv')
    obv = pandas.DataFrame(obv)
    obv["Reg"] = sm.OLS(obv["Obv"],sm.add_constant(range(len(obv.index)),prepend=True)).fit().fittedvalues 
    return obv

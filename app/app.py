from flask import Flask, render_template, url_for
from datas import datas
from simpleCache import simpleCache
import os.path
from nvd3.lineChart import lineChart
from flask.templating import render_template_string
from logic import logic
from util import htmlCleaner

app = Flask(__name__,static_url_path='')
 
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/close/<string:ticker_symbol>', methods=['GET'])
def close(ticker_symbol):
    
    ticker_symbol = ticker_symbol.lower()
    isCached = simpleCache.checkSimpleCache("cache-close/",ticker_symbol)
    
    if isCached == True:
        cached = simpleCache.readSimpleCache("cache-close/",ticker_symbol)
        print "load close from cache"
        return render_template_string(cached)
    else:
        _file = ticker_symbol+'.h5'
        _location = "files/" 
        datas.download(ticker_symbol,_file,_location)
        if(os.path.exists(_location+_file)):
            
            df = datas.toDataFrame(_location,_file,ticker_symbol)
            df = logic.buildClose(df)
            type = "lineChart"
            chart = lineChart(name=type, x_is_date = False)
           
            xdata = []
            ydata= []
            regr = []
            
            ydata = df.Close.tail(255)
            regr = df.Reg.tail(255)
            
            for i in range(0,len(ydata)):
                xdata.append(i)
        
            kwargs1 = {'color': 'black','height':300}
            extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " calls"}}
            chart.add_serie(y=ydata, x=xdata, name='Close', extra=extra_serie, **kwargs1)
            extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " calls"}}
            chart.add_serie(y=regr, x=xdata, name='Reg', extra=extra_serie, **kwargs1)
            chart.buildhtml()
            html = chart.htmlcontent
            html = htmlCleaner.htmlCleaner(html, "close")
            simpleCache.writeSimpleCache("cache-close/",ticker_symbol,html)
            print "load from df"
            return render_template_string(html)
    
        else:
            return "empty space - load empty space into div -"

@app.route('/obv/<string:ticker_symbol>', methods=['GET'])
def obv(ticker_symbol):
    
    ticker_symbol = ticker_symbol.lower()
    isCached = simpleCache.checkSimpleCache("cache-obv/",ticker_symbol)
    
    if isCached == True:
        cached = simpleCache.readSimpleCache("cache-obv/",ticker_symbol)
        print "load obv from cache"
        return render_template_string(cached)
    else:
        _file = ticker_symbol+'.h5'
        _location = "files/" 
        datas.download(ticker_symbol,_file,_location)
        if(os.path.exists(_location+_file)):
           
            df = datas.toDataFrame(_location,_file,ticker_symbol)
            df = logic.buildObv(df)
            type = "lineChart"
            chart = lineChart(name=type, x_is_date = False)
           
            xdata = []
            ydata= []
            
            ydata = df.Obv.tail(255)
            regr = df.Reg.tail(255)
            
            for i in range(0,len(ydata)):
                xdata.append(i)
        
            kwargs1 = {'color': 'black','height':300}
            extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " calls"}}
            chart.add_serie(y=ydata, x=xdata, name='Obv', extra=extra_serie, **kwargs1)
            extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " calls"}}
            chart.add_serie(y=regr, x=xdata, name='Reg', extra=extra_serie, **kwargs1)
            chart.buildhtml()
            html = chart.htmlcontent
            html = htmlCleaner.htmlCleaner(html, "obv")
            simpleCache.writeSimpleCache("cache-obv/",ticker_symbol,html)
            print "load from df"
            return render_template_string(html)
    
        else:
            return "empty space - load empty space into div -"


@app.route('/div/<string:ticker_symbol>', methods=['GET'])
def div(ticker_symbol):
    
    ticker_symbol = ticker_symbol.lower()
    isCached = simpleCache.checkSimpleCache("cache-div/",ticker_symbol)
    
    if isCached == True:
        cached = simpleCache.readSimpleCache("cache-div/",ticker_symbol)
        print "load div from cache"
        return render_template_string(cached)
    else:
        _file = ticker_symbol+'.h5'
        _location = "files/" 
        datas.download(ticker_symbol,_file,_location)
        if(os.path.exists(_location+_file)):
           
            df = datas.toDataFrame(_location,_file,ticker_symbol)
            df = logic.buildDiv(df)
            type = "lineChart"
            chart = lineChart(name=type, x_is_date = False)
           
            xdata = []
            ydata= []
            
            ydata = df.Div.tail(255)
            line = df.Line.tail(255)
            
            for i in range(0,len(ydata)):
                xdata.append(i)
        
            kwargs1 = {'color': 'black','height':300}
            extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " calls"}}
            chart.add_serie(y=ydata, x=xdata, name='Div', extra=extra_serie, **kwargs1)
            chart.add_serie(y=line, x=xdata, name='Zero', extra=extra_serie, **kwargs1)
            chart.buildhtml()
            html = chart.htmlcontent
            html = htmlCleaner.htmlCleaner(html, "div")
            simpleCache.writeSimpleCache("cache-div/",ticker_symbol,html)
            print "load from df"
            return render_template_string(html)
    
        else:
            return "empty space - load empty space into div -"


if __name__ == '__main__':
    app.run(debug=True, port=80)
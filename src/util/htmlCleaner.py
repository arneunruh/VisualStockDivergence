from bs4 import BeautifulSoup
from slimmer import html_slimmer, js_slimmer


def htmlCleaner(html,value):

    soup = BeautifulSoup(html)

    soup.html.unwrap()
    soup.head.extract()
    soup.body.unwrap()

    html = str(soup)
    html = html.replace("<!DOCTYPE html>", "")
    html = html.replace('id="linechart"','id="linechart-'+value+'"');
    html = html.replace('#linechart','#linechart-'+value)
    html = html_slimmer(html)
    html = js_slimmer(html, hardcore = True)
    return html
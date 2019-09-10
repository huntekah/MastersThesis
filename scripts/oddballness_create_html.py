#!/usr/bin/env python 
import os,sys
sys.path.append("../emacsGpt2Extension")
#print(os.getcwd())
#print(sys.path)
from gpt2_proba_engine import proba_engine
from colorsys import hsv_to_rgb
import fileinput
from time import time
#from random import randint

class create_html():
    def __init__(self, text=None):
        self.set_text(text)
        self.engine = proba_engine(text)
        self.html_parts = []

    def set_text(self, text):
        self.text = text

    def create_whole_html(self):

        html_text = self._create_html_header()
        for html_part in self.html_parts:
            html_text += html_part
            html_text = self._append_new_line(html_text)
        html_text = self._create_html_footer(html_text)

        return html_text

    def create_html_part(self, text=None):
        html_text = ""
        self.engine.get_cumulative_search_result(text)
        for token_data in self.engine.token_array:
            print(token_data)
            html_text += '<span style="color: rgb({:.2f},{:.2f},{:.2f})'.format(*self._color_red_green(token_data["oddballness"]))\
                    + '">'\
                    + token_data["name"].replace("\n","</br>")\
                    + '</span> '
        self.html_parts.append(html_text)
        
    @staticmethod
    def _create_html_header():
        html_text = """<!doctype html>

        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>The oddballness</title>
            <meta name="this site allows users to see highlighted oddballness" content="Highlighted oddballness">
            <meta name="K.J. and F.G." content="SitePoint">
        </head>

        <body>"""
        return html_text

    @staticmethod
    def _create_html_footer(html_text):
        html_text += "</body></html>"
        return html_text

    @staticmethod
    def _append_new_line(html_text):
        html_text += "</br>"
        return html_text

    @staticmethod
    def _color_red_green(val):
        starthue = 120
        stophue = 0
        minval = 0.0
        maxval = 1.0
        h = (float(val-minval) / (maxval-minval)) * (stophue-starthue) + starthue
        r, g, b = hsv_to_rgb(h/360, 1., 1.)
        return r*255, g*255, b*255

if __name__ == "__main__":
    html_parsing_engine = create_html()
    lines = ""
    text_limit = 1024
    for line in fileinput.input():
        if len(lines) + len(line) < text_limit:
            lines += line
        else:
            html_parsing_engine.create_html_part(lines)
            lines = line[0:text_limit]
    else:
        html_parsing_engine.create_html_part(lines)

    html = html_parsing_engine.create_whole_html()
    #print(html)
    time_stamp = int(time())
    file_name ="gpt2_parsed_document_{}.html".format(time_stamp)
    with open(file_name, "w+") as f:
        f.write(html)
    print("The result have been saved to {}".format(file_name))
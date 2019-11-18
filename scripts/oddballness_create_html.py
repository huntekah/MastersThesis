#!/usr/bin/env python3.7
import os,sys
sys.path.append("../backend")
from proba_engines import Gpt2OddballnessEngine
from colorsys import hsv_to_rgb
import fileinput
from time import time

class create_html():
    r"""
    Constructs a BertTokenizer.
    :class:`~pytorch_transformers.BertTokenizer` runs end-to-end tokenization: punctuation splitting + wordpiece

    Args:
        vocab_file: Path to a one-wordpiece-per-line vocabulary file
        do_lower_case: Whether to lower case the input. Only has an effect when do_wordpiece_only=False
        do_basic_tokenize: Whether to do basic tokenization before wordpiece.
        max_len: An artificial maximum length to truncate tokenized sequences to; Effective maximum length is always the
            minimum of this value (if specified) and the underlying BERT model's sequence length.
        never_split: List of tokens which will never be split during tokenization. Only has an effect when
            do_wordpiece_only=False
    """

    def __init__(self, text=None, color_threshold = 0.5):
        r"""

        :param text:
        :param color_threshold:
        """
        self.set_text(text)
        self.engine = Gpt2OddballnessEngine(text)
        self.html_parts = []
        self.color_threshold = color_threshold

    def set_text(self, text):
        r"""

        :param text:
        :return:
        """
        self.text = text

    def create_whole_html(self):
        r"""

        :return:
        """
        html_text = self._create_html_header()
        for html_part in self.html_parts:
            html_text += html_part
            html_text = self._append_new_line(html_text)
        html_text = self._create_html_footer(html_text)

        return html_text

    def create_html_part(self, text=None):
        r"""

        :param text:
        :return:
        """
        html_text = ""
        self.engine.get_sentence_oddballness(text)
        for token_data in self.engine.sentence_data:
            #print(token_data)
            html_text += '<span style="color: rgb({:.2f},{:.2f},{:.2f})'.format(*self._color_from_value(token_data["oddballness"]))\
                    + '">'\
                    + token_data["name"].replace("\n","</br>")\
                    + '</span> '
        self.html_parts.append(html_text)
        
    @staticmethod
    def _create_html_header():
        r"""

        :return:
        """
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
        r"""

        :param html_text:
        :return:
        """
        html_text += "</body></html>"
        return html_text

    @staticmethod
    def _append_new_line(html_text):
        r"""

        :param html_text:
        :return:
        """
        html_text += "</br>"
        return html_text

    def _color_from_value(self, val):
        r"""

        :param val:
        :return:
        """
        if val > self.color_threshold:
            starthue = 60
            stophue = 0
            minval = self.color_threshold
            maxval = 1.0
            h = (float(val-minval) / (maxval-minval)) * (stophue-starthue) + starthue
            r, g, b = hsv_to_rgb(h/360, 1., 1.)
            return r*255, g*255, b*255
        return 0,0,0

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
    print(html)
    time_stamp = int(time())
    file_name ="gpt2_parsed_document_{}.html".format(time_stamp)
    with open(file_name, "w+") as f:
        f.write(html)
    #print("The result have been saved to {}".format(file_name))

#!/usr/bin/env python
import os, sys

sys.path.append("../backend")
from gpt2_proba_engine import proba_engine
from colorsys import hsv_to_rgb
import fileinput
from time import time

def mock_post():
    query = "Alice has a Cat.<|endofsentence|>"
    engine = proba_engine(query)
    json_response = engine.get_text_correction_proposal(query)
    print(json_response)

if __name__ == "__main__":
    mock_post()
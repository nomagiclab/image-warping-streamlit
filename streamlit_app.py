from io import BytesIO
import PIL.Image
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import urllib
import cv2

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

def write_image(dg, arr):
    arr = np.uint8(np.clip(arr/255.0, 0, 1)*255)
    dg.image(arr, use_column_width=True)
    return dg


@st.cache()
def read_file_from_url(url):
    return urllib.request.urlopen(url).read()


MAX_IMG_WIDTH = 600
MAX_IMG_HEIGHT = 400
DEFAULT_IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/commons/5/59/Brama_G%C5%82%C3%B3wna_kampus_centralny_Uniwersytetu_Warszawskiego_2019.jpg'


file_obj = st.sidebar.file_uploader('Choose an image:', ('jpg', 'jpeg'))

if not file_obj:
    file_obj = BytesIO(read_file_from_url(DEFAULT_IMAGE_URL))

img_in = PIL.Image.open(file_obj)

img_in.thumbnail((MAX_IMG_WIDTH, MAX_IMG_HEIGHT), PIL.Image.ANTIALIAS)
img_in = np.float32(img_in)

rows,cols,channels = img_in.shape

M00 = st.sidebar.slider("M00", 0., 3., 1.)
M01 = st.sidebar.slider("M01", 0., 3., 0.)
M02 = st.sidebar.slider("M02", 0, 200, 0)

M10 = st.sidebar.slider("M10", 0., 3., 0.)
M11 = st.sidebar.slider("M11", 0., 3., 1.)
M12 = st.sidebar.slider("M12", 0, 200, 0)

with st.echo(code_location='below'):
    M = np.float32([[M00, M01, M02],[M10, M11, M12]])
    dst = cv2.warpAffine(img_in,M,(cols,rows))

st.write(M)
write_image(st, img_in)
write_image(st, dst)

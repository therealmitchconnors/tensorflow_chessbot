import numpy as np
import PIL.Image
import glob
import os

# Imports for visualization
import PIL.Image
from cStringIO import StringIO
import urllib2

# Imports for pulling metadata from imgur url
import requests
from bs4 import BeautifulSoup

def loadImageFromURL(img_url):
  """Load PIL image from URL, keep as color"""
  req = urllib2.Request(img_url, headers={'User-Agent' : "TensorFlow Chessbot"})
  con = urllib2.urlopen(req)
  return PIL.Image.open(StringIO(con.read()))

def loadImageFromPath(img_path):
  """Load PIL image from image filepath, keep as color"""
  return PIL.Image.open(open(img_path,'rb'))

def loadImageURL(image_url):
  """Load image from url.
  Or metadata url link from imgur"""

  # If imgur try to load from metadata
  if 'imgur' in image_url:
    img = loadImgur(image_url)
    if img:
      return img

  # Otherwise try loading image from url directly
  try:
    return loadImageFromURL(image_url)
  except IOError, e:
    pass

  return None

def loadImgur(image_url):
  """Get metadata head image url from given imgur url"""
  soup = BeautifulSoup(requests.get(image_url).content, "lxml")

  # Get metadata tags
  meta = soup.find_all('meta')
  # Get the specific tag, ex.
  # <meta content="https://i.imgur.com/bStt0Fuh.jpg" name="twitter:image"/>
  tags = list(filter(lambda tag: 'name' in tag.attrs and tag.attrs['name'] == "twitter:image", meta))
  if tags == []:
    return None

  # Load image from metadata url
  url = tags[0]['content']
  print("Found imgur metadata URL:", url)
  return loadImageFromURL(url)

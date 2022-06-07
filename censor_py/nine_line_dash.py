import torch
import cv2
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
from urllib.request import urlopen
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

def nine_line_dash_check(user_id, image_url, nineLineModel, mapModel, censor_coll):
  results = nineLineModel(image_url)
  results.names# or .show()
  boxes = results.xyxy[0].tolist()

  if len(boxes) >0:
    censor_coll.insert_one({
          "user_id": user_id,
          "url": image_url,
          "type_of_censoring": "Nine-Line-Dash"
        })
    return "nine"
  else:
    img = Image.open(urlopen(image_url))
    img = np.array(img)
    img = np.expand_dims(img, axis = 0)
    if np.argmax(mapModel.predict(img)[0]) == 0:
      censor_coll.insert_one({
          "user_id": user_id,
          "url": image_url,
          "type_of_censoring": "Map"
        })
      return "map"
    else:
      return "SAFE"
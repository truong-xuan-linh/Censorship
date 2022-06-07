import os
import gdown
from nudenet import NudeDetector
import matplotlib.pyplot as plt
from PIL import Image
from urllib.request import Request, urlopen
import numpy as np
import pymongo
import argparse
from PIL import Image

def NSFW_check(user_id, image_url, censor_coll, detector):

    img = Image.open(urlopen(image_url))
    img = np.array(img)
    
    results = detector.detect(img, min_prob= 0.4)
    sf = ""
    check = ["EXPOSED_BREAST_F", "EXPOSED_GENITALIA_F", "EXPOSED_GENITALIA_M"]
    for rs in results:
      if rs["label"] in check:
        censor_coll.insert_one({
          "user_id": user_id,
          "url": image_url,
          "type_of_censoring": "NSFW"
        })
        return True
    return False
#!/usr/bin/python3
import os
import logging
import pytz
import datetime
try:
  ROOT_dir = os.environ['CENSOR_DATA']
except:
  os.environ['CENSOR_DATA'] = "/censor_storage"
  ROOT_dir = os.environ['DEEPFACE_DATA']

try:
  with open(os.path.join(ROOT_dir, "log.txt"), "a") as f:
    f.write("\n-------------------------------------RUN-------------------------------------------\n")
    f.close()
except:
  with open(os.path.join(ROOT_dir, "log.txt"), "w+") as f:
    f.write("\n-------------------------------------RUN-------------------------------------------\n")
    f.close()
# def timetz(*args):
#     return datetime.datetime.now(tz).timetuple()
# tz = pytz.timezone("Asia/Ho_Chi_Minh") # UTC, Asia/Shanghai, Europe/Berlin
logging.Formatter.converter = logging.Formatter.converter = lambda *args: datetime.datetime.now(tz=pytz.timezone('Asia/Ho_Chi_Minh')).timetuple()
logging.basicConfig(filename=os.path.join(ROOT_dir, "log.txt"), level=logging.INFO, format = '[%(asctime)s] - [%(levelname)s] - %(message)s',
                  filemode="a")

try:
  import gdown
  from nudenet import NudeDetector
  import matplotlib.pyplot as plt
  from PIL import Image
  from urllib.request import Request, urlopen
  import numpy as np
  import pymongo
  import argparse
  from PIL import Image
  from NSFW import NSFW_check
  from nine_line_dash import nine_line_dash_check
  import torch
  from tensorflow.keras.models import load_model
  from kafka import KafkaConsumer
  import json
  def main(user_id, image_url, detector, nine_line_model, map_model, censor_coll, logging):
      
      check = NSFW_check(user_id, image_url, censor_coll, detector)
      if check:
        logging.info(f"Find NSFW in picture of user {user_id}")
      else:
        nine = nine_line_dash_check(user_id, image_url, nine_line_model, map_model, censor_coll)
        logging.info(f"Find {nine} in picture of user {user_id}")
  if __name__ == "__main__":
    ROOT_dir = os.environ['CENSOR_DATA']
    uri = "mongodb+srv://truong-xuan-linh:hahalolo@deepface.ky81b.mongodb.net/test"
    try:
      # os.mkdir("/root/.NudeNet/")
      gdown.download("https://drive.google.com/uc?id=110FMuimWZrAIWbkUZnEVV99urDao3xoO", "/root/.NudeNet/detector_v2_base_checkpoint.onnx", quiet=False)
      gdown.download("https://drive.google.com/uc?id=1ySI0UEWzSsrz4rH2UBipnA3FpkbV5Ifu", "/root/.NudeNet/classes", quiet=False) 
    except:
      pass
    if "nine_line_dash.pt" not in os.listdir(ROOT_dir):
        gdown.download("https://drive.google.com/uc?id=10cIHDtvMcM9ZwBjhGIDztT_rSHtmVm6l", os.path.join(ROOT_dir,"nine_line_dash.pt"), quiet=False)
        gdown.download("https://drive.google.com/uc?id=1eGCcv6T1cxnoWs10H3fEXzsITjYIxu98", os.path.join(ROOT_dir,"map.h5"), quiet=False)


    nine_line_model = torch.hub.load(ROOT_dir, 'custom', path=os.path.join(ROOT_dir,"nine_line_dash.pt"), source="local", verbose=False) 
    map_model = load_model(os.path.join(ROOT_dir,"map.h5"))
    client = pymongo.MongoClient(uri)
    mydb = client["test"]
    censor_coll = mydb["censor"]

    detector = NudeDetector("base")

    consumer = KafkaConsumer(bootstrap_servers = '10.10.15.72:9092,10.10.15.73:9092,10.10.15.74:9092',
    group_id= 'group_social_consumer',
    auto_offset_reset =  'latest',
    security_protocol =  'SASL_PLAINTEXT',
    sasl_mechanism = 'SCRAM-SHA-512',
    sasl_plain_username  =  'admin-hahalolo',
    sasl_plain_password  =  'Hahalolo@2021'
    )
    consumer.subscribe(["topic_halo_m200_rep_sync_media"])
    for message in consumer:
      msg = json.loads(message.value.decode("utf-8"))
      user_id = msg["fullDocument"]["pn100"]
      url = msg["fullDocument"]["mv206"]
      main(user_id, url, detector, nine_line_model, map_model, censor_coll, logging)
except Exception as e:
  logging.error(e) 
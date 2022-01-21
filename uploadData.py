import base64
import json
import os
import time

import requests

def make_request_body(ts, conf_score, violation_types, location, image_path):
    if not isinstance(ts, int):
        raise TypeError("ts must be int")
    if not isinstance(conf_score, float):
        raise TypeError("conf_score must be float")
    if not isinstance(violation_types, list):
        raise TypeError("violations_types must be a list")
    if not os.path.exists(image_path):
        raise ValueError("invalid image path")
    body = dict()
    body["timestamp"] = ts
    body["confidenceScore"] = conf_score
    body["violationTypes"] = violation_types
    body["mediaType"] = "JPG"
    body["location"] = location
    if body["mediaType"].lower() != image_path.split(".")[-1]:
        raise ValueError("only jpg images are supported")
    with open(image_path, "rb") as f:
        body["encodedImage"] = base64.b64encode(f.read())
    return body

def main():
    camera_id = "livetestcam"
    url = "https://mpy2xu3546.execute-api.ap-south-1.amazonaws.com/upload"
    ts = int(time.time()*1000)
    conf_score = 0.8
    violation_types = ["gown", "mask"]
    location = "store"
    image_path = "test_img.jpg"
    body = make_request_body(ts, conf_score, violation_types, location, image_path)
    body["cameraId"] = camera_id
    resp = requests.post(url, json=body)
    if resp.status_code != 200:
        print(f"request failed with statuscode = {resp.status_code} and message = {resp.text}")
    else:
        print(resp.text)


if __name__ == "__main__":
    main()

import json
import os
import transformers
from torchvision import transforms
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoTokenizer, BartModel
from datasets import load_dataset
import base64
import gzip
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
from PyQt5 import QtSvg, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QStylePainter

dataset = load_dataset("oliveirabruno01/shaped-svgs-small-unlabeled-900")

# Load the BLIP model
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
tok = AutoTokenizer.from_pretrained("Salesforce/blip-image-captioning-large")
def generate_caption(image):
    img = processor(image, return_tensors="pt")
    caption = model.generate(**img, max_length=512, do_sample=True, temperature=0.5, top_p=0.95)
    return tok.decode(caption[0], skip_special_tokens=True)

ds = open("shaped-svgs-small-labeled.jsonl", "w")
count = 0

total = len(dataset["train"])

app = QtGui.QGuiApplication([])

# Create a QPixmap to render the SVG to
pixmap = QtGui.QPixmap(512,512)
pixmap.fill(QtCore.Qt.transparent)

# Create a QPainter to paint on the QPixmap
painter = QtGui.QPainter(pixmap)

for row in dataset["train"]:
    data = {
        "svg_gzip_b64": "",
        "png_b64": ""
    }
    svg = row["text"].split("```")[1] + "".join(row["text"].split("```")[2:])
    if svg.startswith("svg\n"):
        svg = svg[4:]
    f = open("temp.svg", "w")
    f.write(svg)
    f.flush()
    f.close()
    svg = QtSvg.QSvgRenderer("temp.svg")
    svg.render(painter)
    painter.end()
    pixmap.save("temp.png")
    pixmap.fill(QtCore.Qt.transparent)
    painter.begin(pixmap)
    img = Image.open('temp.png')
    img = img.convert("RGB")
    data["caption"] = generate_caption(img)
    data["svg_gzip_b64"] = base64.b64encode(gzip.compress(row["text"].encode(), 9)).decode()
    tpng = open("temp.png", "rb")
    tpng.seek(0, os.SEEK_END)
    end = tpng.tell()
    tpng.close()
    bts = b''
    png = open("temp.png", "rb")
    while png.tell() < end:
        dat = png.read(1024)
        bts += dat
        bts = bts[:len(dat)-1]
    png.close()
    data["png_b64"] = base64.b64encode(bts).decode()
    ds.write(json.dumps(data) + "\n")
    print(json.dumps(data))
    ds.flush()
    print(f"processed {count} rows os {total}. {count/total*100:.2f}% complete.")
    count += 1
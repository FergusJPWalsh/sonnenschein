# OCR Latin text in PNG images
# Adapted from https://github.com/wjbmattingly/ocr_python_textbook

import pytesseract
import cv2
import numpy as np
import re
import os, glob

def normalise_latin(string):
    """Normalise Latin language character set."""
    norm_string = re.sub("ã|à|ā|â", "a", string)
    norm_string = re.sub("é|è|ē|ę|ê", "e", norm_string)
    norm_string = re.sub("ì|ī|ĩ|î", "i", norm_string)
    norm_string = re.sub("ĳ", "ii", norm_string)
    norm_string = re.sub("õ|ò|ō|ô", "o", norm_string)
    norm_string = re.sub("ũ|ù|ū|û", "u", norm_string)
    norm_string = re.sub("đ", "d", norm_string)
    norm_string = re.sub("ǣ|ǽ|æ", "ae", norm_string)
    norm_string = re.sub("Æ", "AE", norm_string)
    norm_string = re.sub("œ", "oe", norm_string)
    norm_string = re.sub("Œ", "OE", norm_string)
    norm_string = re.sub("ſ", "s", norm_string)
    norm_string = re.sub("&", "et", norm_string)
    return norm_string

def transcribe(page_number):
    img = cv2.imread(f"orig/ora_maritima_png/ora_maritima_scan_latin_only-{page_number}.png")
    img_copy = img.copy()
    greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(greyscale, (15, 15), -1)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernal_e = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 2))
    kernal_d = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 6))
    dilate = cv2.dilate(thresh, kernal_d, iterations=5)
    # cv2.imwrite("orig/dilate_test.png", dilate)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0] + cv2.boundingRect(x)[1] * img.shape[1])
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if h > 30 and w > 300:
            roi = img_copy[y:y+h, x:x+w]
            cv2.rectangle(img, (x,y), (x+w, y+h), (36,255,12), 12)
    # cv2.imwrite("orig/roi_test.png", img)
    ocr_result = pytesseract.image_to_string(img_copy, lang="lat+eng")
    ocr_result = normalise_latin(ocr_result)
    return ocr_result

page_numbers = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"] #, "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54"]
ocr_outputs = []
for i in page_numbers:
    ocr_output = transcribe(i)
    ocr_output = normalise_latin(ocr_output)
    ocr_outputs.append(ocr_output)
    print(f"Page {i} done.")
with open("orig/ora_maritima_transcription.txt", "w", encoding="utf-8") as text_file:
    for output in ocr_outputs:
        text_file.write(f"{output}\n")
print("Finished!\a")
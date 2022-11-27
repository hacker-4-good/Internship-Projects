import streamlit as st
import PyPDF2 as pdf
from textblob import TextBlob
import pytesseract
import os

wdFormatPDF = 17

option = st.selectbox("Select the option: ",("Choose option","PDF","Text","JPG/JPEG"))

file = st.file_uploader("Upload Document")

path = st.text_input("Copy the document path")

if(st.button("Submit")):

    if(option=="PDF"):
        PDF = pdf.PdfFileReader(file)
        for i in range(PDF.numPages):
            res = TextBlob(PDF.getPage(i).extract_text()).correct()
            st.text(res)
            st.text("page {}".format(i))

    if(option=="Text"):
        with open(file.name) as f:
            res = TextBlob(f.readline()).correct()
            st.text(res)
    
    if(option=="JPG/JPEG"):
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        # string = pytesseract.image_to_string("C:\\Users\\mayan\\Downloads\\{}".format(file.name))
        string = pytesseract.image_to_string(path)
        res = TextBlob(string).correct()
        st.text(res)
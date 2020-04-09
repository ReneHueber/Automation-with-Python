import os
import time
from PyPDF2 import PdfFileReader

print(time.localtime(os.path.getmtime("/home/ich/Downloads/Rechnung_Bundesheer_Köpfe.pdf")))

with open("/home/ich/Downloads/Rechnung_Bundesheer_Köpfe.pdf", "rb") as file:
    pdf = PdfFileReader(file)
    pdf_info = pdf.getDocumentInfo()

    for key in pdf_info:
        print("{0}:     {1}".format(key, pdf_info[key]))

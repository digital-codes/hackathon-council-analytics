import os
from rainbow_tqdm import tqdm
import time
from pdf2image import convert_from_path
import pytesseract

# Need to install:
# sudo apt update
# sudo apt install tesseract-ocr
# sudo apt install libtesseract-dev
# sudo apt-get install tesseract-ocr-deu

path = "/root/data/heidelberg_all_pdfs/"

files = [f for f in os.listdir(path) if f.endswith('.pdf')]

start = time.time()
for f in tqdm(files):
    pdf_path = os.path.join(path, f)

    images = convert_from_path(pdf_path, dpi=300)

    md_text = ""
    for img in images:
        text = pytesseract.image_to_string(img, lang='deu')  # ggf. 'eng' oder andere Sprache
        md_text += text + "\n\n"

    md_filename = f.replace('.pdf', '.txt')
    md_path = os.path.join(path, md_filename)
    
    with open(md_path, 'w', encoding='utf-8') as f_new:
        f_new.write(md_text)
        
end = time.time()
print(f"Fertig! Gesamtverarbeitungszeit: {end - start:.2f} Sekunden.")

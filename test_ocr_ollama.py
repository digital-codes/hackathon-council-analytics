from ollama_ocr import OCRProcessor
import os
from rainbow_tqdm import tqdm
import time

# Initialize OCR processor
ocr = OCRProcessor(model_name='granite3.2-vision')

path = "/media/ncdata/__groupfolders/4/TestDocuments/"

files = [f for f in os.listdir(path) if f.endswith('.pdf')]

start = time.time()
for f in tqdm(files[:4]):
    print(f)
    # Erstellen des vollständigen Pfads zur PDF-Datei
    pdf_path = os.path.join(path, f)
    
    # OCR-Prozess mit den gewünschten Parametern
    result = ocr.process_image(
        image_path=pdf_path,
        preprocess=True,
        format_type="markdown",
        language="German"
    )
    
    md_filename = f.replace('.pdf', '.md')
    md_path = os.path.join(path, md_filename)
    
    with open(md_path, 'w', encoding='utf-8') as f_new:
        f_new.write(result)
        
end = time.time()
print(f"Fertig! Gesamtverarbeitungszeit: {end - start:.2f} Sekunden.")

# # Initialize OCR processor
# ocr = OCRProcessor(model_name='granite3.2-vision', max_workers=16)  # max workers for parallel processing

# # Process multiple images
# # Process multiple images with progress tracking
# batch_results = ocr.process_batch(
#     input_path="/media/ncdata/__groupfolders/4/TestDocuments/",  # Directory or list of image paths
#     format_type="markdown",
#     recursive=False,  # Search subdirectories
#     preprocess=True,  # Enable image preprocessing
#     # custom_prompt="Extract all text, focusing on dates and names.", # Optional custom prompt
#     language="German" # Specify the language of the text inserted into the system prompt
# )
# # Access results
# for file_path, text in batch_results['results'].items():
#     print(f"\nFile: {file_path}")
#     # Save the extracted markdown text into a file with the same name as the input
#     output_file = file_path.rsplit('.', 1)[0] + ".md"
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write(text)
#     # print(f"Extracted Text: {text}")

# total_time = time.time() - start
# # Convert total_time to hh:mm:ss format
# formatted_time = time.strftime("%H:%M:%S", time.gmtime(total_time))
# print(f"Time taken: {formatted_time}")
# print(f"Time per document: {total_time / len(batch_results['results']):.2f} seconds")

# # View statistics
# print("\nProcessing Statistics:")
# print(f"Total images: {batch_results['statistics']['total']}")
# print(f"Successfully processed: {batch_results['statistics']['successful']}")
# print(f"Failed: {batch_results['statistics']['failed']}")


algorithms = ["llama3.2-vision:11b", "granite3.2-vision", "moondream", "minicpm-v"]
timing = []
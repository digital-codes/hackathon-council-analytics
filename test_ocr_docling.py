import os
from rainbow_tqdm import tqdm
import time

from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
)


artifacts_path = "../.cache/docling/models/"
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True
pipeline_options.ocr_options.lang = ["de"]
pipeline_options.accelerator_options = AcceleratorOptions(
    num_threads=4, device=AcceleratorDevice.AUTO
)
# pipeline_options.artifacts_path = artifacts_path

path = "/media/ncdata/__groupfolders/4/TestDocuments/"

filepaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.pdf')]

for filepath in tqdm(filepaths, desc="Processing files", unit="file"):
    print(filepath)
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    start_time = time.time()
    conv_result = doc_converter.convert(filepath)
    end_time = time.time() - start_time

    print(f"Document converted in {end_time:.2f} seconds.")

    ## Export results
    doc_filename = filepath.replace('.pdf', '_docling.md')
    md_path = os.path.join(path, doc_filename)
    with open(md_path, "w", encoding="utf-8") as fp:
        fp.write(conv_result.document.export_to_markdown())
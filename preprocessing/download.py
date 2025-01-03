import os
import requests
from tqdm import tqdm
from requests.auth import HTTPBasicAuth
import pymupdf


def download_pdf(folder, idx, verbose=False):
    try:
        content = request_pdf(idx, verbose=verbose)
        if content is not None:
            filename = f'{i}.pdf'
            with open(os.path.join(folder, filename), 'wb') as f:
                f.write(content)
        return True
    except Exception as e:
        print(f"Error for {idx}: {e}")
        return False


def request_pdf(idx, verbose=False):
    """
    Request the PDF file from the municipal council website.
    Returns the content of the file if it's a PDF, otherwise None.
    """
    url = f"https://www.gemeinderat.heidelberg.de/getfile.asp?id={idx}&type=do"
    response = requests.get(url, stream=True)
    
    content_type = response.headers.get('content-type')
    
    if 'application/pdf' in content_type:
        if verbose:
            print(f"PDF found for {idx}.")
        return response.content
    else:
        if verbose:
            print(f"Error: The file retrieved for id {idx} is not a PDF.")
        return None


def extract_text(doc):
	text = ""
	for page in doc:
		text += page.get_text()
	return text


def save_text(text: str, fout: str):
	with open(fout, "w") as f:
		f.write(text)
	return True


if __name__ == '__main__':

    folderPDF = "CouncilDocuments"
    folderTXT = "CouncilTexts"
    txtFiles = [f.strip('.txt') for f in os.listdir(folderTXT) if f.endswith('.txt')]
    pdfFiles = [f.strip('.pdf') for f in os.listdir(folderPDF) if f.endswith('.pdf')]

    n = 0
    for i in tqdm(range(367896, 500000)):
        if str(i) not in txtFiles:
            if str(i) not in pdfFiles:
                download = download_pdf(folderPDF, i, verbose=False)

            fin = os.path.join(folderPDF, f"{i}.pdf")
            fout = os.path.join(folderPDF, f"{i}.txt")
            if os.path.exists(fin) and not os.path.exists(fout):
                doc = pymupdf.open(fin)
                text = extract_text(doc)
                save_text(text, fout)

            n += 1 if download else 0
    print(f"{n} new files downloaded")

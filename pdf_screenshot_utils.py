import fitz  # PyMuPDF
import requests
from io import BytesIO

def pdf_url_to_image(url, id):
    # Download the PDF from the URL
    response = requests.get(url)
    pdf_bytes = BytesIO(response.content)
    
    # Open the PDF
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    # Select the first page
    page = doc.load_page(0)  # 0 is the first page
    
    # Render the page to an image (pixmap)
    pix = page.get_pixmap()
    
    # Save the image to a file
    image_filename = f"imgs/{id}.png"
    pix.save(image_filename)
    
    print(f"Saved first page to {image_filename}")
    return image_filename
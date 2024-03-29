import os
import re
import requests
import tarfile
from latex_utils import get_main_contents
from pdf_screenshot_utils import pdf_url_to_image
from string_rendering import render_paper_contents

def download_arxiv_paper_legacy(url):
    """
    DEPRECATED: This function is deprecated and will be removed in future versions.
    """
    # Regular expression to match the arXiv PDF URL pattern
    arxiv_url_pattern = r'https://arxiv\.org/pdf/(.+)\.pdf'
    
    # Check if the URL matches the expected arXiv PDF URL pattern
    match = re.match(arxiv_url_pattern, url)
    if not match:
        raise ValueError("The URL provided does not match the expected arXiv paper format.")
    
    # Extract the arXiv ID from the URL
    arxiv_id = match.group(1)
    
    # Prepare the directory to save the PDF
    pdf_dir = 'pdfs'
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    # Define the path where the PDF will be saved
    pdf_path = os.path.join(pdf_dir, f"{arxiv_id}.pdf")
    
    # Download the PDF
    response = requests.get(url)
    if response.status_code == 200:
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        return pdf_path
    else:
        raise Exception("Failed to download the paper. Please check the URL and try again.")

# BUILDING THE FUNCTION TO DOWNLOAD THE LATEX SOURCE CODE

def arxiv_id_from_url(url):
    arxiv_url_pattern = r'https://arxiv\.org/pdf/(.+)\.pdf'
    match = re.match(arxiv_url_pattern, url)
    if not match:
        raise ValueError("The URL provided does not match the expected arXiv paper format.")
    return match.group(1)

def download_arxiv_latex(id):
    tar_url = f"https://arxiv.org/src/{id}"
    destination = f"arxiv_srcs/{id}.tar.gz"
    response = requests.get(tar_url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)
    print(f"Download completed: {destination}")
    return destination

def extract_tar_file(source, destination):
    with tarfile.open(source, 'r:gz') as tar:
        tar.extractall(path=destination)
    print(f"Extraction completed to: {destination}")

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File deleted: {file_path}")
    else:
        print("The file does not exist")

# PUTTING IT ALL TOGETHER
def download_arxiv_paper(url):
    arxiv_id = arxiv_id_from_url(url)
    tar_path = download_arxiv_latex(arxiv_id)
    directory_path = f"arxiv_srcs/{arxiv_id}"
    extract_tar_file(tar_path, directory_path)
    delete_file(tar_path)
    return arxiv_id, directory_path

# After executing the code above, we have a folder with the LaTeX source code of the paper. We should now extract the important text from the source files. 

def identify_most_important_tex_file(directory_path):
    tex_files = []
    # Only look at the .tex files in the top level of the directory
    for file in os.listdir(directory_path):
        if file.endswith(".tex"):
            tex_files.append(file)
    if len(tex_files) == 0:
        raise Exception("No .tex files found in the directory")
    if len(tex_files) == 1:
        return tex_files[0]
    elif "main.tex" in tex_files:
        return "main.tex"
    else: 
        raise Exception("Unable to identify. Something else is needed.")
    
# Now we can extract the main contents from the identified .tex file using the get_main_contents function from the latex_utils module.  
def identify_sections_to_send_for_summary(tex_file_path):
    main_contents = get_main_contents(tex_file_path)
    total_length = 0
    final_contents = []
    skip_until_conclusion = False
    for section, content, length in main_contents:
        print(f"Section: {section}")
        print(f"Length: {length}")
        print("\n")
        if total_length + length > 15000:
            skip_until_conclusion = True
            print("Skipping until conclusion...")
        
        if "Conclusion" in section or "Acknowledgments" in section:
            total_length += length
            print("Reached conclusion. Stopping.")
            break
        
        if not skip_until_conclusion:
            final_contents.append((section, content))
            total_length += length

    print(f"Total length: {total_length}")
    return final_contents, total_length

# Convert to TWITTER THREAD :rocket:
def convert_to_twitter_thread(sections):
    from openai_api import create_chat_completion
    user_message = render_paper_contents(sections)
    system_message = None
    with open("system_prompt.txt", "r") as file:
        system_message = file.read()
    thread = create_chat_completion(user_message, system_message, turbo=False)
    return thread

# Finally, we can put all the pieces together to download an arXiv paper, extract the main contents, and identify the sections to send for a summary.
def twitter_thread_summary(url):
    from typefully import create_tweet
    id, directory_path = download_arxiv_paper(url)
    tex_file = identify_most_important_tex_file(directory_path)
    tex_file_path = os.path.join(directory_path, tex_file)
    final_contents, total_length = identify_sections_to_send_for_summary(tex_file_path)
    thread_response = convert_to_twitter_thread(final_contents)
    drafted_thread = thread_response.choices[0].message.content
    print(f"Thread:\n\n{drafted_thread}")
    img_path = pdf_url_to_image(url, id)

    content = f"Instant twitter threads explaining arXiv papers! 🧵👇\n\nLink to paper: {url}\n\n\n\n{drafted_thread}"
    typefully_response = create_tweet(content)
    print(f"Link: {typefully_response['share_url']}")
    return typefully_response, img_path

if __name__ == "__main__":
    # Example URL of an arXiv paper
    url = 'https://arxiv.org/pdf/2403.18802.pdf'
    try:
        pdf_path = download_arxiv_paper(url)
        print(f"PDF saved to: {pdf_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
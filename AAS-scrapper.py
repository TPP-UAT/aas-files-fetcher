import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import logging
import PyPDF2
import random

# All revision from volumes 954 to 932/2 downloaded
base_url = 'https://iopscience.iop.org'
initial_url = "https://iopscience.iop.org/issue/2041-8205/932/1"
final_volume = '928'

#If there is no such folder, the script will create one automatically
downloads_folder_location = r'./webscraping'
if not os.path.exists(downloads_folder_location):os.mkdir(downloads_folder_location)

# If pdf doesn't load, we can append here to try again later
failed_urls = []

# Logging, change log level if needed
logging.basicConfig(filename='data_scrapper.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('my_logger')

# Logging variables
amount_downloaded = 0

# Headers info
cookie_page = '__uzma=250512ea-6c1e-40bf-8e6e-478a89ef6011; __uzmb=1693769734; __uzme=5358; __uzmc=921651035608; __uzmd=1693769734; AWSALB=cNaYVDFWQ5BVqjh1alDPopskEPh0ydidZpVgI8bxm6aB7NoB920sGVV7+wLDcBfFzH3ojgUC3i/N+cjRvm+fc/6n+TOn4FsZvbnKrRjeXT2ic35V/P5aUCmmzmMx; AWSALBCORS=cNaYVDFWQ5BVqjh1alDPopskEPh0ydidZpVgI8bxm6aB7NoB920sGVV7+wLDcBfFzH3ojgUC3i/N+cjRvm+fc/6n+TOn4FsZvbnKrRjeXT2ic35V/P5aUCmmzmMx; JSESSIONID=0AEE3D1229D3E12E2B5AEAE8ECBB5F3C; IOP_session_live=%2F%2F1693769735119%7C99c5ffa6-a19a-4604-a73f-af1a564c674d%7C05292692-e03a-4bed-835a-a18564f6a68d%7C%7C%7C%7C%7C%7C%7C%7C%7Cguest%2F8cb22c50956eb682405e1e462b965959; _ga_XRBV54S80C=GS1.1.1693769736.1.0.1693769736.0.0.0; _ga=GA1.2.797773494.1693769737; _gid=GA1.2.80733584.1693769737; _gat_UA-2254461-36=1; cebs=1; _hjSessionUser_209243=eyJpZCI6IjhjZmFjNTY0LTIyNmYtNWUyOC05NDA4LTIzNWIyMTljYzI0YyIsImNyZWF0ZWQiOjE2OTM3Njk3MzY4NDQsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample_209243=0; _hjSession_209243=eyJpZCI6ImVjNDdhODRjLWMzN2ItNDg0Zi1hNGQ1LTdjYzlmNmQ3NmVlMCIsImNyZWF0ZWQiOjE2OTM3Njk3MzY4NDUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ce.clock_event=1; _ce.clock_data=105%2C181.23.196.40%2C1%2C6d797a3d21eb30c3af058ab3a2bf562d; cebsp_=1; _ce.s=v11.lhb~1693769737672~lcw~1693769737672~v~2ad825add0612d36c1c7036a39e7b427eafd4c11~vpv~0~v11.fhb~1693769737671~lcw~1693769737673'
cookie_pdf = '__uzma=250512ea-6c1e-40bf-8e6e-478a89ef6011; __uzmb=1693769734; __uzme=5358; JSESSIONID=0AEE3D1229D3E12E2B5AEAE8ECBB5F3C; IOP_session_live=%2F%2F1693769735119%7C99c5ffa6-a19a-4604-a73f-af1a564c674d%7C05292692-e03a-4bed-835a-a18564f6a68d%7C%7C%7C%7C%7C%7C%7C%7C%7Cguest%2F8cb22c50956eb682405e1e462b965959; _gid=GA1.2.80733584.1693769737; _gat_UA-2254461-36=1; cebs=1; _hjFirstSeen=1; _hjIncludedInSessionSample_209243=0; _hjSession_209243=eyJpZCI6ImVjNDdhODRjLWMzN2ItNDg0Zi1hNGQ1LTdjYzlmNmQ3NmVlMCIsImNyZWF0ZWQiOjE2OTM3Njk3MzY4NDUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ce.clock_event=1; _ce.clock_data=105%2C181.23.196.40%2C1%2C6d797a3d21eb30c3af058ab3a2bf562d; _ga=GA1.2.797773494.1693769737; _hjSessionUser_209243=eyJpZCI6IjhjZmFjNTY0LTIyNmYtNWUyOC05NDA4LTIzNWIyMTljYzI0YyIsImNyZWF0ZWQiOjE2OTM3Njk3MzY4NDQsImV4aXN0aW5nIjp0cnVlfQ==; cebsp_=2; _ce.s=v11.lhb~1693769754814~lcw~1693769737673~v~2ad825add0612d36c1c7036a39e7b427eafd4c11~vpv~0~v11.fhb~1693769737671~lcw~1693769754815; _ga_XRBV54S80C=GS1.1.1693769736.1.1.1693769777.0.0.0; __uzmc=713511675035; __uzmd=1693769776; AWSALB=6WMtbq94orqcGWnYDnAOQL4UHrXC/6wObgeXjviJs+wSITL1+kszBXbZ+oLOE2Sr9LSt+A88i7+omzz1AvVdFeFGpKhIc1lmh+OHaP3YcZ3CQb6NEHUyGSBY+37V; AWSALBCORS=6WMtbq94orqcGWnYDnAOQL4UHrXC/6wObgeXjviJs+wSITL1+kszBXbZ+oLOE2Sr9LSt+A88i7+omzz1AvVdFeFGpKhIc1lmh+OHaP3YcZ3CQb6NEHUyGSBY+37V'

# Different agents for requests
agents = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

# It takes a really long time to make this check, in the meantime can fail the request because of cookies
def requested_captcha(content, pdf_url):
    log.debug("Checking for captcha.....")
    soup = BeautifulSoup(content, "html.parser")
    text_to_find = "We apologize for the inconvenience..."
    if text_to_find in soup.get_text():
        log.error(f"ERROR: Captcha requested in {pdf_url}")
        failed_urls.append(pdf_url)
        return True
    return False

def check_for_captcha(filename):
    try:
        with open(filename, 'rb') as f:
            PyPDF2.PdfReader(f)
    except Exception as e:
        log.error(f"Failed to download {filename}: {e}")
        print(f"Failed to download {filename}")

def download_pdf(pdf_url, folder_location):
    # random_number = random.randint(0, 8)
    headers = {
        'authority': 'iopscience.iop.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,es-AR;q=0.8,es;q=0.7',
        'cache-control': 'max-age=0',
        'referer': 'https://iopscience.iop.org/issue/2041-8205/954/1',
        'cookie': cookie_pdf,
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    try:
        # Name the pdf files using the last portion of each link which are unique in this case
        pdf_id = pdf_url.split('/')[-2]
        file_path = folder_location + '/' + pdf_id + '.pdf'
        session = requests.Session()
        with session.get(pdf_url, headers=headers, timeout=20) as response:
            log.debug("Reading content......")
            request_content = response.content
            with open(file_path, 'wb') as f:
                f.write(request_content)
            check_for_captcha(file_path)
    
    except requests.exceptions.Timeout:
        log.error(f"Request timed out for URL: {pdf_url}. Stopping.")
        failed_urls.append(pdf_url)
    except Exception as e:
        log.error(f"An unexpected error occurred for URL {pdf_url}: {e}")
        failed_urls.append(pdf_url)

def download_pdfs(pdfs_urls, folder_location):
    for pdf_url in pdfs_urls:
        log.debug(f"Downloading pdf from url: {pdf_url}")
        download_pdf(pdf_url, folder_location)
        global amount_downloaded
        amount_downloaded += 1
        log.debug("Finished downloading pdf")
        log.debug("------------------------")
        time.sleep(5)

def get_urls_from_page(beautiful_soup_html): 
    pages_pdfs_urls = []   
    for link in beautiful_soup_html.select("a[href$='/pdf']"):
        # Get the pdf urls
        pages_pdfs_urls.append(urljoin(base_url,link['href']))
    return pages_pdfs_urls

def get_page_html(page_url):
    # Get the raw html from the initial url
    headers = {
        'authority': 'iopscience.iop.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,es-AR;q=0.8,es;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': cookie_page,
        'referer': 'https://iopscience.iop.org/issue/2041-8205/953/2',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    log.debug("-----------------------------------------\n\n\n")
    log.debug(f"Start downloading PDFs from volume: {page_url.split('/')[-2]}, revision {page_url.split('/')[-1]}")
    response = requests.get(page_url, headers=headers)
    log.info(f"Finished requesting page from: {page_url}")

    # Parse the raw html into a BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def create_folder_path_for_page(page_url):
    folder_name = page_url.split('/')[-2] + '-' + page_url.split('/')[-1]
    folder_location = os.path.join(downloads_folder_location, folder_name)
    if not os.path.exists(folder_location):os.mkdir(folder_location)
    return folder_location

def get_all_files_from_page(page_html_object, page_url):
    # Create the folder for the page
    folder_location = create_folder_path_for_page(page_url)

    # Get the pdf urls from the html object
    pdfs_urls = get_urls_from_page(page_html_object)
    log.debug(f"Amount of urls found: {len(pdfs_urls)}")
    log.debug(f"Urls from page: {pdfs_urls}\n")

    # Download the pdfs
    download_pdfs(pdfs_urls, folder_location)

def get_all_files_from_pages():
    page_url = initial_url
    is_next_page_useful = True

    while is_next_page_useful:
        # Get the current page files
        page_html_object = get_page_html(page_url)
        get_all_files_from_page(page_html_object, page_url)
        log.info(f"Finished downloading all pdfs from page: {page_url}")

        # Get the next page files
        page_url = get_next_page_url(page_html_object)
        is_next_page_useful = check_next_page_is_useful(page_url)

        if not is_next_page_useful:
            log.info(f"Finished downloading, max volume reached: {final_volume}")

def get_next_page_url(page_html_object):
    try:
        next_page_url = page_html_object.find('a', href=lambda href: href and '/issue/' in href)
        return urljoin(base_url, next_page_url['href'])
    except Exception as e:
        log.error(f"Error getting next page url: {e}")

def check_next_page_is_useful(page_url):
    volume_number = page_url.split('/')[-2]
    return volume_number != final_volume

log.info("---------------------------------------------------------------------------------------------------------------------------\n\n\n\n\n")
log.info(f"Initiating the download of all PDFs from AAS with final volume: {final_volume}")
get_all_files_from_pages()
log.info(f"Finished downloading all pdfs, total amount: {amount_downloaded}")

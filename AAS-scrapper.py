import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import logging
import PyPDF2
import sys
import random

# All revision from volumes 954 to 932/2 downloaded
base_url = 'https://iopscience.iop.org'
initial_url = "https://iopscience.iop.org/issue/0004-637X/951/1"
final_volume = '900'

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
cookie_page = '__uzma=1e5e2d89-a460-4256-8f3a-0aa59a2b5299; __uzmb=1695679366; __uzme=1851; JSESSIONID=26CF35F22C924DA3AD160102B8FD56DD; _hjFirstSeen=1; _hjIncludedInSessionSample_209243=0; _hjSession_209243=eyJpZCI6ImJkZTc3MTM0LWE5ZTUtNGIwMi04NjgzLTUxN2VmYmQ4YmMwZSIsImNyZWF0ZWQiOjE2OTU2NzkzNjk0OTAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gid=GA1.2.1079881102.1695679370; _gat_UA-2254461-36=1; cebs=1; _ce.clock_event=1; _ce.clock_data=76%2C181.23.209.37%2C1%2C6d797a3d21eb30c3af058ab3a2bf562d; IOP_prod_state=b3cd5c19110bbef8d36f83d159134b12b74b4acb5d7a1014eb7addf6778f29b498f8c9d0e595c0837fe1b4efee592dbf5a9877beb561bcb0fad695e10e0e16dbe144eea3ce5af1c5d001ed597f8a7a94c03e56a470596ee25d99be8cd148dc520f07dfa7397c3ec64b716feaf262dfc484cf81aba6f0e8ab572aae; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrUTFORFZGTUVJek5rTXhOMEpCTVRnMFJqazFNMEV5TXpFME56SkZOVEF6UVRrMVFVRkNPUSJ9.eyJodHRwczovL2lvcHAub3JnL2VuY3J5cHRlZCI6ImY4NzlhODczOGNlN2I2NDNjZTMyYzI2NGNmYzUzNDFhM2NmMzJiYWU3MDVkZGY2N2QwNGQyNmRjYWFjYmY4OWNiYzM1NDdiZTYwZTEwYmMwNWE1ODZiYjM1NjU0NDlkNTNkZGZhYTU2NzIzODA1M2FiZDAyOTY4OGQwMTIyOTJlYmQzNDc1MzY4ZDEzOTllZjExZWNiYTk2MTc4OTk1YWZhMGI1YzBmZTk2ZjEyMTcwOTk5Y2Y2MDNjNGNlY2FkZWUwMzZiM2JjOTE2YWE4NjAwMjE5ZTE1NTllMTI1MTcyIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLm15aW9wc2NpZW5jZS5pb3Aub3JnLyIsInN1YiI6ImF1dGgwfDY0ZjMzMWY3MDU1ZGZkZjVjZWZlMjFhMCIsImF1ZCI6WyJodHRwczovL3NlY3VyZWxvZ2luLmNsZC5pb3Aub3JnIiwiaHR0cHM6Ly9teWlvcHNjaWVuY2UuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5NTY3OTM4MCwiZXhwIjoxNjk1NzY1NzgwLCJhenAiOiJDRjJZSlF6NkI1VnQxU3ppQklHRzBlVklmMHlkQzVVSyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUiLCJwZXJtaXNzaW9ucyI6W119.kFm_Up6G0G0e9kM8c35K8a7jqdpWLu6i_ix4SXHyaPXSK4vflMzfRp982ec2Mkt6GOuUi7gZfNcpbxOTcL3wV3zHMhMNh57OQkabnWl0Eyw6sn_b7FyJLXUqe0Cdy4cVZ5QErwbHF-7QqJnHadqrIBX8ZeGyNfZ69Mwv2mXyGzmbA_T09pM8mlv7WQuURprulE0X_ccBMsHHUP2T-KXINYvO8jGfte6PS2_Njh1D0OQ5wfxAMM3iDL2AGSvFV8tzimlvRXEQOkBATLxbkUkEQnBs7tXSs-giaualAGWovbdzliVsMnGWNys0e1BsmQXyHQwZU1aJWgScjB-NHzgUKQ; IOP_session_live=cn%253Dauth0%257C64f331f7055dfdf5cefe21a0%252C%2F%2F1695679381051%7Ceef20c4e-87ba-49d1-b825-ec708a86f9fe%7C8b2b2d51-085f-4e29-a90a-1f0e88918c1f%7C%7C%7C%7C%7C%7C%7C%7C%7Cguest%2F8f145fe4ad1e882bd83ea2484d5408f7; __uzmc=128251388996; __uzmd=1695679381; AWSALB=g6qgAeIoY65X2QmflxHLM3ZuxuZpz++RnrdTsFCIc0EMlKCg7IjBTZ/y2LKfe5NQeUeBbrq9YnF98I6Ufx/4JSHYnSUZ+UKH0EdzGtrKLgREqUuw51JvMmZ+cbPu; AWSALBCORS=g6qgAeIoY65X2QmflxHLM3ZuxuZpz++RnrdTsFCIc0EMlKCg7IjBTZ/y2LKfe5NQeUeBbrq9YnF98I6Ufx/4JSHYnSUZ+UKH0EdzGtrKLgREqUuw51JvMmZ+cbPu; _ga_XRBV54S80C=GS1.1.1695679369.1.1.1695679383.0.0.0; _ga=GA1.2.967314126.1695679369; _hjSessionUser_209243=eyJpZCI6IjExM2Q3YWFhLTBjZmQtNWQ0YS04ODllLWJjZWQ0M2M4ZmZlMSIsImNyZWF0ZWQiOjE2OTU2NzkzNjk0ODksImV4aXN0aW5nIjp0cnVlfQ==; cebsp_=2; _ce.s=v~c9f0822c83a7a4310b373eaaa02887cd6b9196b9~lcw~1695679370253~vpv~0~v11.fhb~1695679370252~v11.lhb~1695679384132~lcw~1695679384133'
cookie_pdf = '__uzma=1e5e2d89-a460-4256-8f3a-0aa59a2b5299; __uzmb=1695679366; __uzme=1851; JSESSIONID=26CF35F22C924DA3AD160102B8FD56DD; _hjFirstSeen=1; _hjIncludedInSessionSample_209243=0; _hjSession_209243=eyJpZCI6ImJkZTc3MTM0LWE5ZTUtNGIwMi04NjgzLTUxN2VmYmQ4YmMwZSIsImNyZWF0ZWQiOjE2OTU2NzkzNjk0OTAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gid=GA1.2.1079881102.1695679370; _gat_UA-2254461-36=1; cebs=1; _ce.clock_event=1; _ce.clock_data=76%2C181.23.209.37%2C1%2C6d797a3d21eb30c3af058ab3a2bf562d; IOP_prod_state=b3cd5c19110bbef8d36f83d159134b12b74b4acb5d7a1014eb7addf6778f29b498f8c9d0e595c0837fe1b4efee592dbf5a9877beb561bcb0fad695e10e0e16dbe144eea3ce5af1c5d001ed597f8a7a94c03e56a470596ee25d99be8cd148dc520f07dfa7397c3ec64b716feaf262dfc484cf81aba6f0e8ab572aae; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrUTFORFZGTUVJek5rTXhOMEpCTVRnMFJqazFNMEV5TXpFME56SkZOVEF6UVRrMVFVRkNPUSJ9.eyJodHRwczovL2lvcHAub3JnL2VuY3J5cHRlZCI6ImY4NzlhODczOGNlN2I2NDNjZTMyYzI2NGNmYzUzNDFhM2NmMzJiYWU3MDVkZGY2N2QwNGQyNmRjYWFjYmY4OWNiYzM1NDdiZTYwZTEwYmMwNWE1ODZiYjM1NjU0NDlkNTNkZGZhYTU2NzIzODA1M2FiZDAyOTY4OGQwMTIyOTJlYmQzNDc1MzY4ZDEzOTllZjExZWNiYTk2MTc4OTk1YWZhMGI1YzBmZTk2ZjEyMTcwOTk5Y2Y2MDNjNGNlY2FkZWUwMzZiM2JjOTE2YWE4NjAwMjE5ZTE1NTllMTI1MTcyIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLm15aW9wc2NpZW5jZS5pb3Aub3JnLyIsInN1YiI6ImF1dGgwfDY0ZjMzMWY3MDU1ZGZkZjVjZWZlMjFhMCIsImF1ZCI6WyJodHRwczovL3NlY3VyZWxvZ2luLmNsZC5pb3Aub3JnIiwiaHR0cHM6Ly9teWlvcHNjaWVuY2UuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5NTY3OTM4MCwiZXhwIjoxNjk1NzY1NzgwLCJhenAiOiJDRjJZSlF6NkI1VnQxU3ppQklHRzBlVklmMHlkQzVVSyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUiLCJwZXJtaXNzaW9ucyI6W119.kFm_Up6G0G0e9kM8c35K8a7jqdpWLu6i_ix4SXHyaPXSK4vflMzfRp982ec2Mkt6GOuUi7gZfNcpbxOTcL3wV3zHMhMNh57OQkabnWl0Eyw6sn_b7FyJLXUqe0Cdy4cVZ5QErwbHF-7QqJnHadqrIBX8ZeGyNfZ69Mwv2mXyGzmbA_T09pM8mlv7WQuURprulE0X_ccBMsHHUP2T-KXINYvO8jGfte6PS2_Njh1D0OQ5wfxAMM3iDL2AGSvFV8tzimlvRXEQOkBATLxbkUkEQnBs7tXSs-giaualAGWovbdzliVsMnGWNys0e1BsmQXyHQwZU1aJWgScjB-NHzgUKQ; IOP_session_live=cn%253Dauth0%257C64f331f7055dfdf5cefe21a0%252C%2F%2F1695679381051%7Ceef20c4e-87ba-49d1-b825-ec708a86f9fe%7C8b2b2d51-085f-4e29-a90a-1f0e88918c1f%7C%7C%7C%7C%7C%7C%7C%7C%7Cguest%2F8f145fe4ad1e882bd83ea2484d5408f7; _hjSessionUser_209243=eyJpZCI6IjExM2Q3YWFhLTBjZmQtNWQ0YS04ODllLWJjZWQ0M2M4ZmZlMSIsImNyZWF0ZWQiOjE2OTU2NzkzNjk0ODksImV4aXN0aW5nIjp0cnVlfQ==; __uzmc=116431675915; __uzmd=1695679386; AWSALB=rO6KYqUOZXwEQ2vfxGvAmxwAo1M+6//8iJEG0hWcyQpFrA47CaEcgfC1CgSnNzrDLKOgo3OjrEOs2x6LW0XsoYKV6PQoKbSVC5kNdgybYcCsoAy8xN6xunjLyQHH; AWSALBCORS=rO6KYqUOZXwEQ2vfxGvAmxwAo1M+6//8iJEG0hWcyQpFrA47CaEcgfC1CgSnNzrDLKOgo3OjrEOs2x6LW0XsoYKV6PQoKbSVC5kNdgybYcCsoAy8xN6xunjLyQHH; _ga=GA1.2.967314126.1695679369; cebsp_=3; _ce.s=v~c9f0822c83a7a4310b373eaaa02887cd6b9196b9~lcw~1695679384133~vpv~0~v11.fhb~1695679370252~v11.lhb~1695679389832~lcw~1695679389833; _ga_XRBV54S80C=GS1.1.1695679369.1.1.1695679402.0.0.0'

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

def check_for_captcha(filename, count_downloaded, total_page):
    try:
        with open(filename, 'rb') as f:
            PyPDF2.PdfReader(f)
    except Exception as e:
        log.error(f"Failed to download {filename}: {e}. Missing: {total_page - count_downloaded}")
        print(f"Failed to download {filename}. Missing: {total_page - count_downloaded}")
        sys.exit(1)

def download_pdf(pdf_url, folder_location, count_downloaded, total_page):
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
            check_for_captcha(file_path, count_downloaded, total_page)
    
    except requests.exceptions.Timeout:
        log.error(f"Request timed out for URL: {pdf_url}. Stopping.")
        failed_urls.append(pdf_url)
    except Exception as e:
        log.error(f"An unexpected error occurred for URL {pdf_url}: {e}")
        failed_urls.append(pdf_url)

def download_pdfs(pdfs_urls, folder_location, count_downloaded, total_page):
    for pdf_url in pdfs_urls:
        log.debug(f"Downloading pdf from url: {pdf_url}")
        download_pdf(pdf_url, folder_location, count_downloaded, total_page)
        global amount_downloaded
        amount_downloaded += 1
        count_downloaded += 1
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
    count_downloaded = 0
    # Create the folder for the page
    folder_location = create_folder_path_for_page(page_url)

    # Get the pdf urls from the html object
    pdfs_urls = get_urls_from_page(page_html_object)
    log.debug(f"Amount of urls found: {len(pdfs_urls)}")
    log.debug(f"Urls from page: {pdfs_urls}\n")

    # Download the pdfs
    download_pdfs(pdfs_urls, folder_location, count_downloaded, len(pdfs_urls))

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

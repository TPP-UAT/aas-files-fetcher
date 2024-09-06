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
base_url = 'https://iopscience.iop.org/'
initial_url = "https://iopscience.iop.org/issue/0004-637X/864/1"
final_volume = '850'

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
cookie_page = '__ssds=2; __uzmaj2=4671fcbf-6c1b-4d41-8285-fd43f8dbe470; __uzmbj2=1693657627; cebs=1; __ssuzjsr2=a9be0cd8e; cebsp_=95; _ce.s=v~2fce4bd2471c2defc8a58192aea6733f16716a4c~lcw~1699319250038~vpv~0~v11.fhb~1699207439220~v11.lhb~1699319250036~v11.cs~215584~v11.s~b1a7f800-7c05-11ee-8ffe-5b8572c1e4a2~v11.sla~1699208368308~v11.send~1699319305839~lcw~1699319305841; __uzma=a978636f-fa60-4ca1-8fef-1b7ccbad2178; __uzmb=1710275299; __uzme=5247; __uzmcj2=8572231037709; __uzmdj2=1710367809; cookieyes-consent=consentid:dFlDNndHSUp1TkJYSEZ3THdYdjNXaXJmTWs3Y0Q0bnI,consent:yes,action:yes,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,lastRenewedDate:1711555514000; hum_iopp_visitor=014a535c-86e7-47f7-a386-5bce30276646; _hjSessionUser_209243=eyJpZCI6Ijk2ZGRkZTQzLWI5YjUtNThkMC05YmQ2LWNkYTBhNWZmMjg3NSIsImNyZWF0ZWQiOjE3MjQxMDc2NzU0NjEsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.59258425.1725491901; hum_iopp_synced=true; __gads=ID=106ed6f57c3e2245:T=1710367661:RT=1725496804:S=ALNI_MbG5wWKRWHkwQSa0GD9WGJmJjSjPg; __gpi=UID=00000a12d393ebaa:T=1710367661:RT=1725496804:S=ALNI_Ma_R9XbHPp1hFSBZiXi05xiKIRzlw; __eoi=ID=d0654398b1c7071a:T=1710367661:RT=1725496804:S=AA-AfjauufztcQOtuTF7KNFBg2T_; JSESSIONID=54AEC898071E161D793A8499424634F0; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrUTFORFZGTUVJek5rTXhOMEpCTVRnMFJqazFNMEV5TXpFME56SkZOVEF6UVRrMVFVRkNPUSJ9.eyJodHRwczovL2lvcHAub3JnL2VuY3J5cHRlZCI6ImQyOTk1MTFkNWIzNDAwZGRhNGUwNWM0MTdhODNlZDBkZTAzMTI3ZWVhMTNhZGQ4ZGNmMTA4ZTQwMTNhYmZjMWVlZjFhZjRiNjJmYWFmMGVlMzc3ZjJkMjlmOTU4ZTk0YTMxZmU2MTU1MTQ4NGY0NDY1ZmZlNjYzMDU0YjI2OTQ0MjY2ZDNhMDQzOGFiZjExMjA3YmNkYmYyYTNmODQ3NjQ1YzEyNGEyYjU3ZmUzZWIzN2ViODVkNTllMWRjMWYyMDFhNjRhYTRiOGI0MWZlNDBkOWEwNzNmMTVlNTNiOGFjIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLm15aW9wc2NpZW5jZS5pb3Aub3JnLyIsInN1YiI6ImF1dGgwfDY0ZjMyZTIzZDNiNTk3NTQwOWNkNjg3MiIsImF1ZCI6WyJodHRwczovL3NlY3VyZWxvZ2luLmNsZC5pb3Aub3JnIiwiaHR0cHM6Ly9teWlvcHNjaWVuY2UuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcyNTU3NjQ5OCwiZXhwIjoxNzI1NjYyODk4LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIiwiYXpwIjoiQ0YyWUpRejZCNVZ0MVN6aUJJR0cwZVZJZjB5ZEM1VUsiLCJwZXJtaXNzaW9ucyI6W119.QXrmmqe7eQi-MaSu215-0-LuwVU83C5qx16w_3KnzlczlfaSuGBavkVzjP6lmbhrXElTGrhPa7_2jXlSuRHbuj7usRaZLouw1W4e33fAATDxhiOBwfp7mClo2zVMrkmxCwzpfq9k3JmJNx_FGuH6LL8dHt_72U6W1mYP30p3QXxatogmlQRq7GvkTqNmDm4PqiTfeoNV0Lsm0BdO4WG5JdpWi91lEooNKkOWVpwdbD3k2Ek-tjZE5Ealcwn2f08xjgXAiYTJXobeLKfWcQKYfmCd8Oik4383Wpo18LfDG4rwzHmLIgj4iGRFR9x7D7LmGekg-AbnRmd98mV5OdmMZQ; IOP_session_live=cn%253Dauth0%257C64f32e23d3b5975409cd6872%252C%2F%2F1725576499079%7C9043357b-327e-48a7-927f-8d1daf6e52ec%7Cf68933d4-eb55-46ba-a52c-7a53ea08a862%7C%7C%7C%7C%7C%7C%7C%7C%7Cguest%2F86625d6897f6c4b3e8ae14ab913a6a26; _ga=GA1.2.1978699474.1724107673; _ga_XRBV54S80C=GS1.1.1725576481.5.1.1725576512.0.0.0; __uzmc=5562214569808; __uzmd=1725576545; __uzmf=7f6000a2a149fc-5a22-43bc-bf9c-de46164270ad172549680307079742838-e82ad8b553bb3e9b52; uzmx=7f90008954c85b-f751-43b8-992a-a8bf03c62a424-171511913414010457411768-69c71c146c25727688; AWSALB=S9oiuJ1n0Su9SqmL3BBpcdz6QdEZovwN9lLFoi3XY2ZyRthUQZG/Sar5IGkc2H/ddzCx2WUTvNKK+MiTwFHXYaKZOvBNSzQlqU1gxmm1ggs8/pCdmRRu26JimOJz; AWSALBCORS=S9oiuJ1n0Su9SqmL3BBpcdz6QdEZovwN9lLFoi3XY2ZyRthUQZG/Sar5IGkc2H/ddzCx2WUTvNKK+MiTwFHXYaKZOvBNSzQlqU1gxmm1ggs8/pCdmRRu26JimOJz'
cookie_pdf = '__ssds=2; __uzmaj2=4671fcbf-6c1b-4d41-8285-fd43f8dbe470; __uzmbj2=1693657627; cebs=1; __ssuzjsr2=a9be0cd8e; cebsp_=95; _ce.s=v~2fce4bd2471c2defc8a58192aea6733f16716a4c~lcw~1699319250038~vpv~0~v11.fhb~1699207439220~v11.lhb~1699319250036~v11.cs~215584~v11.s~b1a7f800-7c05-11ee-8ffe-5b8572c1e4a2~v11.sla~1699208368308~v11.send~1699319305839~lcw~1699319305841; __uzma=a978636f-fa60-4ca1-8fef-1b7ccbad2178; __uzmb=1710275299; __uzme=5247; __uzmcj2=8572231037709; __uzmdj2=1710367809; cookieyes-consent=consentid:dFlDNndHSUp1TkJYSEZ3THdYdjNXaXJmTWs3Y0Q0bnI,consent:yes,action:yes,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,lastRenewedDate:1711555514000; hum_iopp_visitor=014a535c-86e7-47f7-a386-5bce30276646; _hjSessionUser_209243=eyJpZCI6Ijk2ZGRkZTQzLWI5YjUtNThkMC05YmQ2LWNkYTBhNWZmMjg3NSIsImNyZWF0ZWQiOjE3MjQxMDc2NzU0NjEsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.59258425.1725491901; hum_iopp_synced=true; __gads=ID=106ed6f57c3e2245:T=1710367661:RT=1725496804:S=ALNI_MbG5wWKRWHkwQSa0GD9WGJmJjSjPg; __gpi=UID=00000a12d393ebaa:T=1710367661:RT=1725496804:S=ALNI_Ma_R9XbHPp1hFSBZiXi05xiKIRzlw; __eoi=ID=d0654398b1c7071a:T=1710367661:RT=1725496804:S=AA-AfjauufztcQOtuTF7KNFBg2T_; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrUTFORFZGTUVJek5rTXhOMEpCTVRnMFJqazFNMEV5TXpFME56SkZOVEF6UVRrMVFVRkNPUSJ9.eyJodHRwczovL2lvcHAub3JnL2VuY3J5cHRlZCI6ImQyOTk1MTFkNWIzNDAwZGRhNGUwNWM0MTdhODNlZDBkZTAzMTI3ZWVhMTNhZGQ4ZGNmMTA4ZTQwMTNhYmZjMWVlZjFhZjRiNjJmYWFmMGVlMzc3ZjJkMjlmOTU4ZTk0YTMxZmU2MTU1MTQ4NGY0NDY1ZmZlNjYzMDU0YjI2OTQ0MjY2ZDNhMDQzOGFiZjExMjA3YmNkYmYyYTNmODQ3NjQ1YzEyNGEyYjU3ZmUzZWIzN2ViODVkNTllMWRjMWYyMDFhNjRhYTRiOGI0MWZlNDBkOWEwNzNmMTVlNTNiOGFjIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLm15aW9wc2NpZW5jZS5pb3Aub3JnLyIsInN1YiI6ImF1dGgwfDY0ZjMyZTIzZDNiNTk3NTQwOWNkNjg3MiIsImF1ZCI6WyJodHRwczovL3NlY3VyZWxvZ2luLmNsZC5pb3Aub3JnIiwiaHR0cHM6Ly9teWlvcHNjaWVuY2UuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcyNTU3NjQ5OCwiZXhwIjoxNzI1NjYyODk4LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIiwiYXpwIjoiQ0YyWUpRejZCNVZ0MVN6aUJJR0cwZVZJZjB5ZEM1VUsiLCJwZXJtaXNzaW9ucyI6W119.QXrmmqe7eQi-MaSu215-0-LuwVU83C5qx16w_3KnzlczlfaSuGBavkVzjP6lmbhrXElTGrhPa7_2jXlSuRHbuj7usRaZLouw1W4e33fAATDxhiOBwfp7mClo2zVMrkmxCwzpfq9k3JmJNx_FGuH6LL8dHt_72U6W1mYP30p3QXxatogmlQRq7GvkTqNmDm4PqiTfeoNV0Lsm0BdO4WG5JdpWi91lEooNKkOWVpwdbD3k2Ek-tjZE5Ealcwn2f08xjgXAiYTJXobeLKfWcQKYfmCd8Oik4383Wpo18LfDG4rwzHmLIgj4iGRFR9x7D7LmGekg-AbnRmd98mV5OdmMZQ; JSESSIONID=C5EA14BB09742F0FBDC0EFB44B24210A; IOP_session_live=cn%253Dauth0%257C64f32e23d3b5975409cd6872%252C%2F%2F1725590027808%7C39477100-60ee-44d0-b5a5-65d5286eee29%7C30915a93-6bb7-4ec9-9ffb-3c5064a5fdb7%7C%7C%7C%7C%7C%7C%7C%7C%7Cguest%2Fe6f8c9f1b20a918d819f3895696a63c5; _gat_UA-2254461-36=1; _ga_XRBV54S80C=GS1.1.1725590028.6.1.1725590028.0.0.0; _ga=GA1.1.1978699474.1724107673; _hjSession_209243=eyJpZCI6IjdhMjAwN2QxLTRhMzYtNDQzNC05MWJiLWIzZmNhYTQyNGU0ZSIsImMiOjE3MjU1OTAwMjkyODIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; __uzmc=9409815145669; __uzmd=1725590032; __uzmf=7f6000a2a149fc-5a22-43bc-bf9c-de46164270ad172549680307093229022-640b58233e9e0beb58; uzmx=7f90008954c85b-f751-43b8-992a-a8bf03c62a425-171511913414010470897952-57dabc342d1801dc94; AWSALB=BjRTYNeAszMr/+c4+8MGLXoIahlXPTQGNL20iteXEcLpdSqYHSTUgcjF9ZP+6OEyF9v/9jtDUGQ+mPfLibc6yYijjqFQOSIYFrvIxZ9SUB4ZKk5BuMhAxfQGBcAv; AWSALBCORS=BjRTYNeAszMr/+c4+8MGLXoIahlXPTQGNL20iteXEcLpdSqYHSTUgcjF9ZP+6OEyF9v/9jtDUGQ+mPfLibc6yYijjqFQOSIYFrvIxZ9SUB4ZKk5BuMhAxfQGBcAv'

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

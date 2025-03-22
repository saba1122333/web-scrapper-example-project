import requests
from bs4 import BeautifulSoup
from utils import *
from logger import log


def book_scrapper(website, book_link):
    log('info', f'Starting to scrape book at {website}{book_link}')
    try:
        response = requests.get(f'{website}{book_link}')
        response.raise_for_status()

        log('debug', f'Successfully retrieved page for {book_link}')
        soup = BeautifulSoup(response.text, 'html.parser')

        image_src = soup.select_one('img')['src']
        title = soup.select_one('h1').text
        price = soup.select_one('p.price_color').text.replace('Â£', '').strip()
        availability = soup.select_one('p.price_color + p').text.strip()
        image_path = download_image(image_src)

        log('info', f'Successfully scraped book: "{title}"')
        return {
            'title': title,
            'price': float(price),
            'availability': availability,
            'image_src': image_src
        }

    except requests.exceptions.RequestException as e:
        log('error', f'Request failed for {website}{book_link}: {str(e)}')
    except Exception as e:
        log('error', f'Error scraping book at {website}{book_link}: {str(e)}')
        return None


def scrapper(website, page_limit):
    page_limit = min(50, max(page_limit, 1))
    log('info', f'Starting scraper for {website} with limit of {page_limit} pages')
    limiter = 1
    current_page = f"page-{limiter}.html"
    current_url = f'{website}{current_page}'
    books = []

    while limiter <= page_limit:
        try:
            log('info', f'Scraping page {limiter}/{page_limit}: {current_page}')
            response = requests.get(current_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            image_containers = soup.select('ol.row li div.image_container a')
            log('debug', f'Found {len(image_containers)} books on page {limiter}')

            for el in image_containers:
                book_link = el.get('href')
                book = book_scrapper(website, book_link)
                if book:
                    books.append(book)

            next_page = soup.select_one('ul.pager li.next a')['href']
            current_page = next_page
            current_url = f'{website}{current_page}'
            log('info', f'Moving to next page: {current_page}')

        except requests.exceptions.RequestException as e:
            log('error', f'Failed to fetch page {current_page}: {str(e)}')
            break
        except Exception as e:
            log('error', f'Error processing page {current_page}: {str(e)}')
            break
        finally:
            limiter += 1

    log('info', f'Scraping completed. Collected {len(books)} books.')

    if books:
        log('info', 'Creating JSON and CSV files')
        try:
            make_json(books)
            make_csv(books)
            log('info', 'Successfully saved data to JSON and CSV files')
        except Exception as e:
            log('error', f'Failed to save data: {str(e)}')
    else:
        log('warning', 'No books collected, skipping file creation')

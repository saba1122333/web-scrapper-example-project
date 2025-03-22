import json, csv, os

import requests

from logger import log


def make_csv(books, save_dir='booksCsv'):
    log('info', f"Starting CSV creation for {len(books)} books in directory '{save_dir}'")

    if not books:
        log('warning', f"No books data provided, skipping CSV creation")
        return

    if not os.path.exists(save_dir):
        log('info', f"Creating directory '{save_dir}'")
        try:
            os.makedirs(save_dir)
        except Exception as e:
            log('error', f"Failed to create directory '{save_dir}': {str(e)}")
            return

    file_path = os.path.join(save_dir, 'data.csv')
    fieldnames = books[0].keys()

    try:
        log('debug', f"Writing CSV data to {file_path}")
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)
        log('info', f"Successfully created CSV with {len(books)} books at {file_path}")
    except Exception as e:
        log('error', f"Failed to write CSV file: {str(e)}")


def make_json(books, save_dir='booksJson'):
    log('info', f"Starting JSON creation for {len(books)} books in directory '{save_dir}'")

    if not books:
        log('warning', f"No books data provided, skipping JSON creation")
        return

    if not os.path.exists(save_dir):
        log('info', f"Creating directory '{save_dir}'")
        try:
            os.makedirs(save_dir)
        except Exception as e:
            log('error', f"Failed to create directory '{save_dir}': {str(e)}")
            return

    file_path = os.path.join(save_dir, 'data.json')

    try:
        log('debug', f"Writing JSON data to {file_path}")
        with open(file_path, "w") as file:
            json.dump(books, file, indent=4)
        log('info', f"Successfully created JSON with {len(books)} books at {file_path}")
    except Exception as e:
        log('error', f"Failed to write JSON file: {str(e)}")


def download_image(image_src, base_url="https://books.toscrape.com/", save_dir="book_images"):
    log('info', f'Starting to download image: {image_src}')

    if not os.path.exists(save_dir):
        log('info', f'Creating directory: {save_dir}')
        os.makedirs(save_dir)

    # Fix the image URL
    if image_src.startswith('../../'):
        image_src = image_src.replace('../../', '')
        full_url = f"{base_url}{image_src}"
    else:
        full_url = f"{base_url}{image_src}" if not image_src.startswith('http') else image_src

    filename = os.path.basename(image_src)
    save_path = os.path.join(save_dir, filename)

    try:
        log('debug', f'Downloading image from: {full_url}')
        response = requests.get(full_url)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            file.write(response.content)

        log('info', f'Successfully downloaded image to: {save_path}')
        return save_path
    except Exception as e:
        log('error', f'Failed to download image {full_url}: {str(e)}')
        return None

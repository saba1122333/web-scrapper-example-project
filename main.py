from task_3.scrapper import scrapper

website = "https://books.toscrape.com/catalogue/"
if __name__ == '__main__':
    scrapper(website, int(input("Number of Pages to be scraped please enter [1 to 50] : ")))

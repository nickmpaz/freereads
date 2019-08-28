import requests, re
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
 
class BaseMirror(ABC):
 
    @abstractmethod
    def __init__(self): 
        pass

    @abstractmethod
    def search(self, search_term): 
    
        payload = {"req": search_term}
        r = requests.get(self.search_page, params=payload)
        page_content = BeautifulSoup(r.content, "html.parser")
        results = list(page_content.find("table", class_="c").children)[1:]

        book_list = []

        for result in results:

            try:

                id_el = result.td
                author_el = id_el.next_sibling.next_sibling
                title_el = author_el.next_sibling.next_sibling
                publisher_el = title_el.next_sibling.next_sibling
                year_el = publisher_el.next_sibling.next_sibling
                pages_el = year_el.next_sibling.next_sibling
                language_el = pages_el.next_sibling.next_sibling
                size_el = language_el.next_sibling.next_sibling
                extension_el = size_el.next_sibling.next_sibling
                md5 = re.search('md5=([A-Z0-9]*)"', str(title_el)).group(1)
                title = title_el.get_text(separator="\n").splitlines()[0] 
                
                book_list.append({
                    "id": id_el.text,
                    "author": author_el.text,
                    "title": title,
                    "md5": md5,
                    "publisher": publisher_el.text,
                    "year": year_el.text,
                    "pages": pages_el.text,
                    "language": language_el.text,
                    "size": size_el.text,
                    "extension": extension_el.text
                })

            except: continue

        return book_list

    @abstractmethod
    def download(self, book, filename, progress_bar): 

        if progress_bar:
            progress_bar.message = "fetching download..."
            progress_bar.progress = 0 
            progress_bar.draw()

        r = requests.get(self.show_page % book[self.show_field])
        page_content = BeautifulSoup(r.content, "html.parser")
        download_link = page_content.find('a', href=True)
        download = self.download_page % download_link['href']

        

        r = requests.get(download, stream = True) 

        if r.status_code == 200:


            with open(filename, "wb") as download: 
                
                total_length = int(r.headers.get('content-length'))
                current_length = 0
                progress_bar.message = "downloading..."

                for chunk in r.iter_content(chunk_size=64): 
                    if chunk: 
                        download.write(chunk) 
                        current_length += 64
                        if progress_bar:
                            progress_bar.progress = (current_length / total_length) 
                            progress_bar.draw()

            progress_bar.message = "download complete."
            progress_bar.draw()

            return 

class GenLibRus(BaseMirror):

    def __init__(self):
        self.search_page = "http://gen.lib.rus.ec/search.php"
        self.show_page= "http://93.174.95.29/_ads/%s"
        self.show_field = "md5"
        self.download_page = "http://93.174.95.29%s"

    def search(self, search_term):

        return super().search(search_term)

    def download(self, book, filename, progress_bar=False):
        
        return super().download(book, filename, progress_bar)


class LibGen():

    def __init__(self):
        self.mirrors = [
            GenLibRus()
        ]

    def search(self, search_term):
        return self.mirrors[0].search(search_term)

    def download(self, book, filename, progress_bar):
        return self.mirrors[0].download(book, filename, progress_bar)
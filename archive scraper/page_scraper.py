import sqlite3
import requests
from bs4 import BeautifulSoup

def scrap_page(page_url):

    conn = sqlite3.connect('iranjib.db')
    cur = conn.cursor()
    create_table_staement = '''CREATE TABLE IF NOT EXISTS news (
                                    url,
                                    title, 
                                    summary, 
                                    content, 
                                    date, 
                                    views
                                    )'''
    cur.execute(create_table_staement)

    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')
    title = page_soup.find('h1').get_text()
    summary = page_soup.find('div',{'class':'newssummary'}).get_text()
    matn_soup = page_soup.find('div', {'class':'matn'})
    paragraphs = matn_soup.find_all('p')
    news_text = ''
    for p in paragraphs:
        news_text += p.get_text() + '\n'
    table_soup = page_soup.find_all('table')[1]
    tr_soup = table_soup.find_all('tr')[1]
    date = tr_soup.find_all('td')[1].get_text()
    views = tr_soup.find_all('td')[2].get_text()
    insert_statements = '''INSERT INTO news VALUES (?,?,?,?,?,?)'''
    cur.execute(insert_statements, (    page_url,
                                        title, 
                                        summary, 
                                        news_text,
                                        date, 
                                        views ))
    conn.commit()
    conn.close()
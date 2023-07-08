import requests
from bs4 import BeautifulSoup as BS

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 "
                  "Safari/537.36 "
}


def parse_page(url):
    session = requests.Session()
    response = session.get(url=url, headers=headers)
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    with open("index.html") as file:
        src = file.read()

    soup = BS(src, 'html.parser')

    dql_table = soup.find("table", class_="tablepress").find_all("tr")
    dql_table_header = dql_table[0]
    dql_table_rows = dql_table[1:]
    with open('data.csv', 'w') as f:
        try:
            header_1 = dql_table_header.find("th", class_="column-1").text.strip()
            header_2 = dql_table_header.find("th", class_="column-2").text.strip()
            header_3 = dql_table_header.find("th", class_="column-3").text.strip()
            header_4 = dql_table_header.find("th", class_="column-4").text.strip()
            header_5 = dql_table_header.find("th", class_="column-5").text.strip()
            header_6 = dql_table_header.find("th", class_="column-6").text.strip()
            header_7 = dql_table_header.find("th", class_="column-7").text.strip()
            f.write(f'{header_1},{header_2},{header_3},{header_4},{header_5},{header_6},{header_7}\n')

            for item in dql_table_rows:
                col_1 = item.find("td", class_="column-1").text.strip()
                col_2 = item.find("td", class_="column-2").text.strip()
                col_3 = item.find("td", class_="column-3").text.strip()
                col_4 = item.find("td", class_="column-4").text.strip()
                col_5 = item.find("td", class_="column-5").text.strip()
                col_6 = item.find("td", class_="column-6").text.strip()
                col_7 = item.find("td", class_="column-7").text.strip()
                f.write(f'{col_1},{col_2},{col_3},{col_4},{col_5},{col_6},{col_7}\n')
        except Exception:
            print("Failed to create data.csv")

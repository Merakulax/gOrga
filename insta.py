import csv
import json
import pandas as pd

from bs4 import BeautifulSoup
import requests


def main():
    # Read df:
    df = pd.read_csv("postings_mitVid.csv", sep=";", encoding="utf-8-sig")

    csv_file = open('beispiel.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['posting_url', 'profile_url', 'posted_date', 'num_likes', 'num_views','posting_text'])

    # Get Html and posting_url also which post? .
    for index, row in df.iterrows():
        num_likes = None
        num_views = None
        posting_text = None

        html = row["html"]
        posting_url = row["posting_url"]
        #print(html)
        # print(id)
        # print(posting_url)

        # create soup für html
        soup = BeautifulSoup(html, 'lxml')

        pu = soup.find('a', class_="sqdOP yWX7d _8A5w5 ZIAjV")["href"]
        profile_url = f"https://www.instagram.com{pu}"

        # get the date
        posted_d = soup.find('time', class_="_1o9PC")["datetime"][:19]
        n = posted_d.split("T")
        posted_date = " ".join(n)

        # try getting the likes -> if post
        try:
            num_likes = soup.find('div', class_="_7UhW9 xLCgt qyrsm KV-D4 fDxYl T0kll").span.text

        # Else it should be a video -> get the views
        except AttributeError:
            num_views = soup.find_all('div', class_="_7UhW9 xLCgt qyrsm KV-D4 uL8Hv T0kll")[1].text[:-8]


        # Get the posting text
        posting_text = soup.find('span', class_="_7UhW9 xLCgt MMzan KV-D4 se6yk T0kll").text
        print(posting_text)

        try:
            csv_writer.writerow([posting_url, profile_url, posted_date, num_likes, num_views, posting_text])
        except UnicodeEncodeError:
            print("!!!hey, da hat was mit dem encoden nicht funktioniert")
            csv_writer.writerow([posting_url, profile_url, posted_date, num_likes, num_views, None])
    csv_file.close()
    return None


if __name__ == '__main__':
    main()
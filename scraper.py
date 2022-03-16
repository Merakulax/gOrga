import csv

from bs4 import BeautifulSoup #Webscraper
import lxml
import requests # HTTP/ library
import re
#https://edelmut.org/organisationen/page/1/

# Insert the webside link here:
link = lambda page: f"https://edelmut.org/organisationen/page/{page}/"


def get_list_of_links(p_n= 1000):
    """Returns all the links in the website
    :param p_n: if no maximum of pages given then stop at 100
    :return: the list of links
    """

    list_o_links = []

    for i in range(1, p_n+1):
        source = requests.get(link(i)).text
        soup = BeautifulSoup(source, 'lxml')
        test = soup.find('div', id="main").h1.text
        if test == "Fehler 404 – Seite nicht gefunden":
            return list_o_links
        else:
            content = soup.find('ul', class_="geodir-category-list-view clearfix gridview_onefifth geodir-listing-posts geodir-gridview gridview_onefifth")
            for eintrag in content.find_all('li'):
                plink = eintrag.a["href"]
                if plink not in list_o_links:
                    list_o_links.append(plink)
            print(f"Eintrag {i} von {p_n} gelesenn")
    return list_o_links


def get_beschreibungen(content, index, list_of_links):
    """

    :param content: the html of the pagecontent
    :param index: of the link
    :param list_of_links:
    :return: all of the beschreibungen of the organisation
    """
    # All of them are None if not changed
    profil = None
    wirkunskeise = None
    stellenangebote = None
    veranstaltungen = None
    fotos = None
    film = None


    # Notice: those are all not nessesary!
    # check: are they there -> then read them.
    list_of_tabs = [inhalt.text for inhalt in content.find_all('dd')]
    # print(f"liste:: {list_of_tabs} \n")

    if "Profil" in list_of_tabs:
        profil = content.find('li', id="post_contentTab").text
        # print(f"profil: {profil}")

    if "Wirkungskreise" in list_of_tabs:
        wirkunskeise = content.find('li', id="wirkungskreiseTab").text
        # print(f"wirkungskreise: {wirkunskeise}")

    if "Stellenangebote" in list_of_tabs:
        stellenangebote = content.find('li', id="stellenangeboteTab").text
        # print(f"stellenganebote: {stellenangebote}")

    if "Veranstaltungen" in list_of_tabs:
        veranstaltungen = content.find('li', id="gd_eventTab").a['href']
        # print(f"Veranstaltungen : {veranstaltungen}")

    if "Fotos" in list_of_tabs:
        fotos_list = content.find_all('a', class_="geodir-lightbox-image d-block")
        fotos = [f["href"] for f in fotos_list]
        # print(f"Fotots: {fotos}")

    # Film via the edelmut inbetted videos

    if "Film" in list_of_tabs:
        vid = f"{list_of_links[index]}#video"
        film = f"Watch the films here: {vid}"
        # print(film)

    return profil, wirkunskeise, stellenangebote, veranstaltungen, fotos, film



def get_sidebar(sidebar_soup):
    """

    :param sidebar_soup: soup of the sidebar
    :return:
    """
    adress = None
    webside = None
    mail_full = None
    telefone = None
    stellenangebote_sidebar = None
    all_foerderbedarfe = None

    # Get the contents of the sidebar:
    kat = sidebar_soup.find_all('div')
    # print(kat)
    side_e = []
    for sidebar in kat:
        try:
            if sidebar["class"][1] not in side_e:
                side_e.append(sidebar["class"][1])
        except:
            pass
    print(side_e)
    # print(sidebar.prettify())

    # Check each if in sidebar: then get
    if 'geodir-field-address' in side_e:
        street_adress = sidebar_soup.find('span', itemprop="streetAddress").text
        postal_code = sidebar_soup.find('span', itemprop="postalCode").text
        adress_locality = sidebar_soup.find('span', itemprop="addressLocality").text
        adress = f"{street_adress} \n {postal_code} {adress_locality}"
        # print(f"Adresse: {adress}")

    if 'geodir-field-website' in side_e:
        webside = sidebar_soup.find('div', class_="geodir_post_meta geodir-field-website").a["href"]
        # print(f"Webseite: {webside}")

    if 'geodir-field-email' in side_e:
        mail = sidebar_soup.find('div', class_="geodir_post_meta geodir-field-email").a["href"]
        first = mail.split("[")[1]
        second = first.split("]")[0]
        third = second.split(",")
        mail_full = "@".join(third)
        # print(f"E-Mail: {mail_full}")

    if 'geodir-field-phone' in side_e:
        tel = sidebar_soup.find('div', class_="geodir_post_meta geodir-field-phone").a["href"]
        telefone = tel.split("tel:")[1]
        # print(f"Telefon: {telefone} ")

    if 'geodir-field-stellenauswahl' in side_e:
        foerderbedarf = sidebar_soup.find('div', class_="geodir_post_meta geodir-field-stellenauswahl")
        stellenangebote_sidebar = [sa.text for sa in foerderbedarf.find_all('li')]
        # print(f"Stellenangebote: {stellenangebote_sidebar}")

    if 'geodir-field-foerder_auswahl' in side_e:
        st_a = sidebar_soup.find('div', class_="geodir_post_meta geodir-field-foerder_auswahl")
        all_foerderbedarfe = [fb.text for fb in st_a.find_all('li')]
        # print(f"Foerderbedarf: {all_foerderbedarfe}")

    return adress, webside, mail_full, telefone, stellenangebote_sidebar , all_foerderbedarfe


def main():
    """ Main Function
    First open the webside to get all the links
    then scrape the beschreibung and sidebar
    save in a csv

    :return: a csv
    """
    index = 0
    # Do you want to read all of the pages? Or just one?
    n_o_pages = 8
    list_of_links = get_list_of_links(n_o_pages)
    #linksd = ["https://edelmut.org/organisationen/hamburgische-bruecke-gesellschaft-fuer-private-sozialarbeit-e-v/","https://edelmut.org/organisationen/hamburgische-kulturstiftung/"]

    source = (requests.get(links).text for links in list_of_links)
    # print(source)

    # open csv file
    csv_file = open('edelmut_scraper.csv','w', encoding="utf-8")
    csv_writer = csv.writer(csv_file)

    # create header
    csv_writer.writerow(["Organisation", "Adresse", "Webseite", "E-Mail", "Telefonnummer", "Stellenangebote",
                         "Foerderbedarfe","Profil", "Wirkunskreise", "Stellenangebote_Beschreibung",
                         "Veranstaltungen_Beschreibung", "Foto", "Film"])

    soup = (BeautifulSoup(sc, 'lxml') for sc in source)
    for s in soup:
        name_unternehmen = s.find('div', id="main").h1.text
        print(name_unternehmen)

        # We only need the content of the webside
        content = s.find('div', id="main")

        profil, wirkunskreise, stellenangebote, veranstaltungen, fotos, film = get_beschreibungen(content, index, list_of_links)


        # Sidebar:
        # 1. was gibt es überhaupt an der sidebar?  -> contents?
        sidebar = content.find('div', class_="d-block geodir-output-location geodir-output-location-detail")

        adress, webside, mail_full, telefone, stellenangebote_sidebar, all_foerderbedarfe = get_sidebar(sidebar)

        csv_writer.writerow(
            [name_unternehmen, adress, webside, mail_full, telefone, stellenangebote_sidebar, all_foerderbedarfe,
             profil, wirkunskreise, stellenangebote, veranstaltungen, fotos, film])

        # print("\n")
        # print("-----------")
        index = index + 1
    csv_file.close()

    return None


if __name__ == '__main__':
    main()
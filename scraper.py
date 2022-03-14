from bs4 import BeautifulSoup #Webscraper
import lxml
import requests # HTTP/ library
#https://edelmut.org/organisationen/page/1/

# Insert the webside link here:
link = lambda page: f"https://edelmut.org/organisationen/page/{page}/"

links_manuell = ['https://edelmut.org/organisationen/wildfrieden-e-v/', 'https://edelmut.org/organisationen/deutsche-stiftung-fuer-engagement-und-ehrenamt/', 'https://edelmut.org/organisationen/mut-academy-ggmbh/', 'https://edelmut.org/organisationen/schaukelpferd-e-v/', 'https://edelmut.org/organisationen/homann-stiftung/', 'https://edelmut.org/organisationen/michel-stiftung/', 'https://edelmut.org/organisationen/thematanz-e-v/', 'https://edelmut.org/organisationen/bildungsgabe-e-v/', 'https://edelmut.org/organisationen/aktion-baum/', 'https://edelmut.org/organisationen/deutsche-muskelschwund-hilfe-e-v/']

def get_list_of_links(p_n= 100):
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
                plink = eintrag.a ["href"]
                if plink not in list_o_links:
                    list_o_links.append(plink)
            print(f"Eintrag {i} von {p_n} gelesen")
    return list_o_links




def main():
    """

    :return:
    """
    # n_o_pages = 1
    # links_safe = get_list_of_links(n_o_pages)
    # print(links_safe)
    links_safe = links_manuell
    source = (requests.get(links).text for links in links_safe)
    #print(source)

    soup = (BeautifulSoup(sc, 'lxml') for sc in source)
    for s in soup:

        # Notice: those are all not nessesary!
        # check: are they there -> then read them.
        ## 'dd' class_="" -> elemente schauen maybe cases? also mit liste abgehen und wirkungskriese == wirkungskrieseTab finden?
        h = [inhalt.text for inhalt in s.find_all('dd')]
        print(f"liste:: {h} \n")
        if "Profil" in h:
            profil = s.find('li', id="post_contentTab").text
            print(f"profil: {profil}")
        if "Wirkungskreise" in h:
            wirkunskeise = s.find('li', id="wirkungskreiseTab").text
            print(f" wirkungskreise: {wirkunskeise}")

        if "Stellenangebote" in h:
            stellenangebote = s.find('li', id="stellenangeboteTab").text
            print(f"stellenganebote: {stellenangebote}")

        fotos = "link"

        veranstaltungen = ""



        telefonnummer = ""
        Adresse = ""
        E_Mail = ""
        Foerderbedarf = ""


        #info = s.find('div', id="gd_output_location-2")
        #print(info.prettify())









    return None









if __name__ == '__main__':
    main()
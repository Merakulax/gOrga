from bs4 import BeautifulSoup #Webscraper
import lxml
import requests # HTTP/ library
import re
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
                plink = eintrag.a["href"]
                if plink not in list_o_links:
                    list_o_links.append(plink)
            print(f"Eintrag {i} von {p_n} gelesenn")
    return list_o_links




def main():
    """

    :return:
    """
    index = 0
    n_o_pages = 1
    #links_safe = get_list_of_links(n_o_pages)
    # print(links_safe)
    links_safe = links_manuell
    source = (requests.get(links).text for links in links_safe)
    #print(source)

    soup = (BeautifulSoup(sc, 'lxml') for sc in source)
    for s in soup:
        name_unternehmen = s.find('div', id="main").h1.text
        print(name_unternehmen)

        # We only need the content of the webside
        content = s.find('div', id="main")

        # Notice: those are all not nessesary!
        # check: are they there -> then read them.
        list_of_tabs = [inhalt.text for inhalt in content.find_all('dd')]
        print(f"liste:: {list_of_tabs} \n")

        if "Profil" in list_of_tabs:
            profil = content.find('li', id="post_contentTab").text
            print(f"profil: {profil}")

        if "Wirkungskreise" in list_of_tabs:
            wirkunskeise = content.find('li', id="wirkungskreiseTab").text
            print(f"wirkungskreise: {wirkunskeise}")

        if "Stellenangebote" in list_of_tabs:
            stellenangebote = content.find('li', id="stellenangeboteTab").text
            print(f"stellenganebote: {stellenangebote}")

        if "Veranstaltungen" in list_of_tabs:
            veranstaltungen = content.find('li', id="gd_eventTab").a['href']
            print(f"Veranstaltungen : {veranstaltungen}")

        if "Fotos" in list_of_tabs:
            fotos_list = content.find_all('a', class_="geodir-lightbox-image d-block")
            fotos = [f["href"]for f in fotos_list]
            print(f"Fotots: {fotos}")

        # Tuff: also erstmal rausfinden: wie viele filme, welche src
        # man muss einwilligen -> mit scelenium?
        if "Film" in list_of_tabs:
            vid = f"{links_safe[index]}#video"
            film = f"Watch the films here: {vid}"
            print(film)

        # Sidebar:
        # 1. was gibt es überhaupt an der sidebar?  -> contents?

        sidebar = content.find('div', id="gd_output_location-2").text
        print(sidebar)
        print("\n")
        print("-----------")
        # s1 = re.split("Adresse:|E-Mail:|Telefon:|Stellenangebote|Förderbedarf:",sidebar)[1:5]
        """ 
        adresse = s1[0]
        e_mail = s1[1]
        tel = s1[2]
        f_bed = s1[3]
        """
        # List of sidebar things -> wieder mit if "Adresse in list of sidebar things"
        # Adresse
        # Webseite -> Link



        # timer nutzen, schauen ob es sinnvoll ist auf der geanzen webseite zu suchen, oder vorher einen ausschnitt zu
        # erstellen
        # info = s.find('div', id="gd_output_location-2")
        telefonnummer = ""
        Adresse = "mehrere Bestandteile"
        E_Mail = "auch"
        Foerderbedarf = ""


        #print(info.prettify())

        index = index + 1


    return None









if __name__ == '__main__':
    main()
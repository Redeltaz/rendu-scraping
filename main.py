import requests
from bs4 import BeautifulSoup
import requests_cache

requests_cache = requests_cache.install_cache('cache')

class Scraper():
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')

    def get_table_name_and_data(self, div_id):
        full_table = self.soup.find("div", {"id": div_id})
        table_title = full_table.find("div", {"class": "section_heading"})
        table_title = table_title.findChildren("h2")[0].text

        return table_title, full_table

    def get_data_stats(self):
        title, full_table = self.get_table_name_and_data("all_stats_standard")
        
        table_data = full_table.find("table")

        table_title = table_data.find("thead").find_all("tr")[-1].findChildren("th")
        data_titles = [title.text for title in table_title]

        table_data = full_table.find("tbody")
        player_data_list = table_data.findChildren("tr")

        full_data = []
        
        for player_data in player_data_list:
            player_name = player_data.find("th").text
            precise_data_list = player_data.findChildren("td")
            precise_data = [data.text for data in precise_data_list]
            precise_data.insert(0, player_name)

            match_link = precise_data_list[-1].find("a", href=True)["href"]
            precise_data[-1] = match_link

            # link key list and key value in a dict
            player_data = dict(zip(data_titles, precise_data))
            full_data.append(player_data)
        
        return title, full_data

    def get_data_calendar(self):
        title, full_table = self.get_table_name_and_data("all_matchlogs")

        table_data = full_table.find("table")

        table_title = table_data.find("thead").find("tr").findChildren("th")
        data_titles = [title.text for title in table_title]

        calendar_data_list = full_table.find("tbody").findChildren("tr")

        full_data = []
        
        for calendar_data_set in calendar_data_list:
            calendar_data_date = calendar_data_set.find("th").text
            calendar_data = calendar_data_set.findChildren("td")
            for idx, data in enumerate(calendar_data):
                if data.find("a"):
                    data = "{} ({})".format(data.text, data.find("a", href=True)["href"])
                else:
                    data = data.text
                calendar_data[idx] = data
            
            calendar_data.insert(0, calendar_data_date)
            calendar_data = dict(zip(data_titles, calendar_data))
            full_data.append(calendar_data)

        return title, full_data

    def get_data_shoots(self):
        title, full_table = self.get_table_name_and_data("all_stats_shooting")

        table_data = full_table.find("table")
        
        table_title = table_data.find("thead").find_all("tr")[-1].findChildren("th")
        data_titles = [title.text for title in table_title]
        
        shoot_data_list = full_table.find("tbody")
        shoot_data_list = shoot_data_list.findChildren("tr")
        
        full_data = []

        for shoot_data in shoot_data_list:
            player_name = shoot_data.find("th").text
            precise_data_list = shoot_data.findChildren("td")
            precise_data = [data.text for data in precise_data_list]
            precise_data.insert(0, player_name)

            match_link = precise_data_list[-1].find("a", href=True)["href"]
            precise_data[-1] = match_link

            # link key list and key value in a dict
            player_data = dict(zip(data_titles, precise_data))
            full_data.append(player_data)

        return title, full_data

    def get_all_data(self):
        data_stats_title, data_stats_list = self.get_data_stats()
        data_calendar_title, data_calendar_list = self.get_data_calendar()
        data_shoots_title, data_shoots_list = self.get_data_shoots()
        
        return {
            "data_stats": {
                "title": data_stats_title,
                "data": data_stats_list
            },
            "data_calendar": {
                "title": data_calendar_title,
                "data": data_calendar_list
            },
            "data_shoots": {
                "title": data_shoots_title,
                "data": data_shoots_list
            }
        }

if __name__ == "__main__":
    scraper = Scraper("https://fbref.com/fr/equipes/361ca564/Statistiques-Tottenham-Hotspur")
    data = scraper.get_all_data()
    print(data)
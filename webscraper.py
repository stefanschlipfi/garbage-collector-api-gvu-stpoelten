from requests import request
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
from os import getcwd

class GVU_StPoelten:
    def __init__(self,destrict_url):
        if not isinstance(destrict_url,str):
            raise ValueError("destrict_url musst be a string")
        
        self.destrict_url = destrict_url
        self.replace_pattern = '\t?\n?\xa0?'
        self.split_pattern = '\s+'
        self.date_format = '%d.%m.%Y'
        self.working_directory = getcwd()

    def load_page(self):
        """
        load destrict_url
        return response
        """
        return request("GET",self.destrict_url)

    def get_garbage_collector_times(self):
        """
        return formated garbage_collector times
        used request from load_page
        """
        resp = self.load_page()
        if not resp:
            raise resp

        soup = BeautifulSoup(resp.content,features="html5lib")
        time_divs = soup.find_all('div', class_="tunterlegt")

        return_list = list()
        for div_item in time_divs:
            if not len(div_item.contents) == 1:
                raise ValueError("item: {0} has more than one contents".format(div_item))
            item_content = div_item.contents[0]
            return_list.append(re.sub(self.replace_pattern,'',item_content))

        return return_list

    def format_to_json_object(self,get_garbage_collector_times):
        """
        loads from get_garbage_collector_times list
        returns new list with datetime string
        """
        return_list = list()
        for item in get_garbage_collector_times:
            item_list = re.split(self.split_pattern,item)

            #remove Weekday (MO)
            item_list = item_list[1:]
            date = datetime.strptime(item_list[0],self.date_format)

            #standart format
            new_date_string = date.strftime('%Y-%m-%d')

            return_list.append({'date':new_date_string,'garbage_container_type':item_list[1]})

        return return_list

    def json_dump(self,object):
        """
        json dump object to 
        """
        try:
            with open(self.working_directory + '/gvu_stpoelten.json','w') as jf:
                json.dump(object,jf)

        except Exception as e:
            raise e
        else:
            return True

if __name__ == "__main__":
    r = GVU_StPoelten("https://stpoeltenland.umweltverbaende.at/?gem_nr=31917&jahr=2021&kat=32&portal=verband&vb=pl")
    r.json_dump(r.format_to_json_object(r.get_garbage_collector_times()))
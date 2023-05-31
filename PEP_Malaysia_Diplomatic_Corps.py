import httpx
import csv
from bs4 import BeautifulSoup
import re
from urllib import parse
from datetime import datetime


client = httpx.Client(verify=False)
base_url = "https://www.kln.gov.my"

def main():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,ms;q=0.6,ja;q=0.5',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://www.kln.gov.my/web/guest/overseas-mission',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'letter': '',
    }

    print("Start to scrape web...")

    response = client.get('https://www.kln.gov.my/overseas/index.php', params=params, headers=headers)
    souped = BeautifulSoup(response.content, "html.parser")
    li_tags = souped.select("ul#why-choose>li")

    k = 0
    tasks = list()
    for li in li_tags:
        country = li.select_one("div.link").get_text(strip=True, separator=" ")
        containers = li.select("ul.submenu>.container:nth-child(1)")
        for container in containers:
            # address = container.select_one("ul.submenu>.container:nth-child(1) div>div:nth-child(1) li").get_text(strip=True, separator=" ")

            a = container.select_one("li a").get("href", None)

            space_patterns = re.compile(r"\s{2,}/\xa0{1,}")

            result = {
                    "country": country,
                    "head_of_mission": "vacant",
                    "position": "Ambassador (Duta Besar) / Diplomatic Corps of Malaysia (Kor Diplomatik Malaysia) / Ambassador Extraordinary and Plenipotentiary of Malaysia / High Commisioner / Chargé d'Affaires".title(),
                    "photo_link": "",
                    "url": ""
                }

            if a:
                match country.lower():
                    case "algeria":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_520326 > div > p:nth-child(3) > strong > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_520326 > div > p:nth-child(2) > img").get("src", "")
                        position = souped2.select_one("#_101_INSTANCE_2TQe_520326 > div > p:nth-child(4) > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["position"] = space_patterns.sub(" ", position).title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "austria":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_308035 > div > p:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = "Ikram Bin Mohammad Ibrahim".title()
                        result["position"] = "Ambassador Extraordinary and Plenipotentiary of Malaysia to the Republic of Austria, with concurrent accreditation to the Slovak Republic, and Permanent Representative of Malaysia to the United Nations and International Organisations in Vienna".title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "bahrain":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_302883 > div > p:nth-child(5) > strong > span > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_302883 > div > p:nth-child(2) > img").get("src", "")
                        result['head_of_mission'] = name.title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "bangladesh":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_860058 > div > p:nth-child(3)").get_text(strip=True, separator=" ")
                        position = souped2.select_one("#_101_INSTANCE_2TQe_860058 > div > p:nth-child(4)").get_text(strip=True, separator=" ") 
                        result['head_of_mission'] = name.title()
                        result["position"] = space_patterns.sub(" ", position).title()
                        result["url"] = a
                    case "belgium":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_253378 > div > p:nth-child(4) > strong > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_253378 > div > p:nth-child(2) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "bosnia and herzegovina":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_306161 > div > ol > li:nth-child(1) > strong").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "brazil":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_252952 > div > p:nth-child(4) > strong > span > span > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_252952 > div > p:nth-child(2) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "brunei darussalam":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_4202794 > div > p:nth-child(3) > strong > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_4202794 > div > p:nth-child(2) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "cambodia":
                        r = client.get(a.replace("home", "home-based-staff"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_4553456 > div > p:nth-child(5) > span > span > span > strong").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "canada":
                        r = client.get(a.replace("home", "home-based-staff"))
                        r2 = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        souped3 = BeautifulSoup(r2.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_282067 > div > p:nth-child(1) > b").get_text(strip=True, separator=" ")
                        photo = souped3.select_one("#_101_INSTANCE_2TQe_295423 > div > p:nth-child(3) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "chile":
                        r = client.get(a.replace("home", "home-based-staff"))
                        r2 = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        souped3 = BeautifulSoup(r2.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_528305 > div > table > tbody > tr:nth-child(3) > td > p > span > code > span > span").get_text(strip=True, separator=" ")
                        photo = souped3.select_one("#_101_INSTANCE_2TQe_305928 > div > div:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "china":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_251219 > div > p:nth-child(4) > span > span > span > span > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "croatia":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_292767 > div > table:nth-child(4) > tbody > tr > td > p:nth-child(2) > strong").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_292767 > div > table:nth-child(3) > tbody > tr > td > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "cuba":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_384110 > div > p:nth-child(1) > font > span > b").get_text(strip=True, separator=" ")
                        position = souped2.select_one("#_101_INSTANCE_2TQe_384110 > div > p:nth-child(2) > b > span").get_text(strip=True, separator=" ") 
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["position"] = space_patterns.sub(" ", position).title()
                        result["url"] = a
                    case "egypt":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_254973 > div > p:nth-child(1) > strong > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "fiji":
                        r = client.get(a.replace("home", "home-based-staff"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_1450430 > div > p:nth-child(2) > strong").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_1450430 > div > p:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "finland":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_985692 > div > p:nth-child(2) > strong > span > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_985692 > div > p:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "france":
                        r = client.get(a.replace("home", "home-based-staff"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_935983 > div > p:nth-child(2) > strong > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "germany":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_4332829 > div > p:nth-child(7) > span > strong").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_4332829 > div > p:nth-child(6) > strong > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "holy see":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_7689542 > div > p:nth-child(1) > strong").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "hungary":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_254083 > div > div > div > p:nth-child(6) > strong > span > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_254083 > div > div > div > p:nth-child(4) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "iran":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_307099 > div > p:nth-child(4) > font > span > b > i").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_307099 > div > p:nth-child(3) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "japan":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_307569 > div > table > tbody > tr:nth-child(17) > td:nth-child(2) > p > span > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "jordan":
                        r = client.get(a.replace("home", "home-based-staff"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_249911 > div > p:nth-child(4) > span > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).removeprefix("1. ").title()
                        result["position"] = "Ambassador Extraordinary and Plenipotentiary of Malaysia to Jordan and Palestine".title()
                        result["url"] = a
                    case "kazakhstan":
                        result['head_of_mission'] = "H.E. Ambassador Mohd Adli bin Abdullah"
                        result["url"] = a
                    case "kuwait":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_1477494 > div > table > tbody > tr:nth-child(14) > td:nth-child(2)").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "lao people's democratic republic":
                        r = client.get(a.replace("home", "home-based-staff"))
                        r2 = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        souped3 = BeautifulSoup(r2.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_6932817 > div > p:nth-child(3) > strong").get_text(strip=True, separator=" ")
                        photo = souped3.select_one("#_101_INSTANCE_2TQe_308269 > div > p:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "lebanon":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_251443 > div > p:nth-child(1) > strong > span > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "mexico":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_4202203 > div > p:nth-child(1) > span > span > strong").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "morocco":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_304990 > div > div:nth-child(3) > b").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "namibia":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_1414770 > div > p:nth-child(4) > b > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_1414770 > div > p:nth-child(1) > img").get("src", "")
                        position = souped2.select_one("#_101_INSTANCE_2TQe_1414770 > div > p:nth-child(5) > b > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["position"] = space_patterns.sub(" ", position).title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "nepal":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_301476 > div > p:nth-child(5) > b > span").get_text(strip=True, separator=" ")
                        position = souped2.select_one("#_101_INSTANCE_2TQe_301476 > div > p:nth-child(6) > b:nth-child(1) > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["position"] = space_patterns.sub(" ", position).title()
                        result["url"] = a
                    case "netherland":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_307334 > div > div > table > tbody > tr:nth-child(3) > td > p:nth-child(1) > strong").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_1414770 > div > p:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "new zealand":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_321312 > div > p:nth-child(3) > b").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["position"] = "High Commissioner of Malaysia to New Zealand (3 March 2023 - present) Concurrently accredited to Samoa, Cook Islands and Niue.".title()
                        result["url"] = a
                    case "oman":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_1215537 > div > div > div > div > p:nth-child(3) > span > font").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "pakistan":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_385719 > div > table > tbody > tr:nth-child(22) > td:nth-child(2) > p > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "peru":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_302415 > div > p:nth-child(3) > b > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_302415 > div > p:nth-child(2) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "philippines":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_390462 > div > p:nth-child(4) > span > span > strong").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "poland":
                        r = client.get(a.replace("home", "home-based-staff"))
                        r2 = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        souped3 = BeautifulSoup(r2.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_314444 > div > p:nth-child(4) > span").get_text(strip=True, separator=";").split(";")
                        photo = souped3.select_one("#_101_INSTANCE_2TQe_355635 > div > p:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name[0]).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "saudi arabia":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_368454 > div > p:nth-child(17) > strong > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).removeprefix("Current Ambassador: ").title()
                        result["url"] = a
                    case "qatar":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_361002 > div > p:nth-child(3) > span > span").get_text(strip=True, separator=";").split(";")
                        result['head_of_mission'] = space_patterns.sub(" ", name[0]).title()
                        result["url"] = a
                    case "republic of korea":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_371477 > div > p:nth-child(7) > span > strong > span > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "romania":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_4199814 > div > p:nth-child(3) > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).removeprefix("1. ").title()
                        result["url"] = a
                    case "senegal":
                        r = client.get(a.replace("home", "home-based-staff"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_380392 > div > div:nth-child(1) > div:nth-child(3) > strong > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).removeprefix("1. ").title()
                        result["position"] = "Ambassador (Also concurrently to Burkina Faso, Cabo Verde, Republic of The Gambia and Republic of Mali)".title()
                        result["url"] = a
                    case "serbia":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_251812 > div > p:nth-child(3) > span > strong").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_251812 > div > p:nth-child(2) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "singapore":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_296144 > div > table > tbody > tr:nth-child(17) > td:nth-child(1) > span > strong").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "spain":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_374971 > div > table > tbody > tr:nth-child(10) > td > p:nth-child(5) > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "sri lanka":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_1504591 > div > p:nth-child(1) > strong > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "sudan":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_301711 > div > h1 > span > b > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "sweden":
                        r = client.get(a.replace("home", "home-based-staff"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_591259 > div > p:nth-child(4) > span > b > font").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_591259 > div > p:nth-child(3) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["position"] = "Ambassador of Malaysia to Sweden (concurrently accredited to Denmark, Iceland & Norway)".title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "taiwan":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_463350 > div > table > tbody > tr:nth-child(12) > td:nth-child(2) > p > strong > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["position"] = "president".title()
                        result["url"] = a
                    case "thailand":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_211244 > div > p:nth-child(2) > span").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_211244 > div > p:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).replace("-", "").title()
                        result["url"] = a
                        result["photo_link"] = parse.urljoin(base_url, photo)
                    case "timor-leste":
                        r = client.get(a.replace("home", "home-based-staff"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_495591 > div > div > p:nth-child(7) > strong").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).replace("1.", "").title()
                        result["url"] = a
                    case "turkey":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_250425 > div > p:nth-child(4) > strong").get_text(strip=True, separator=" ")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_250425 > div > p:nth-child(3) > img").get("src", "")
                        result['head_of_mission'] = space_patterns.sub(" ", name).replace("-", "").title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "united arab emirates":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_249078 > div > div > p:nth-child(1) > strong > span > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "united kingdom":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_384214 > div > p:nth-child(24) > strong > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).replace("(5/8/2021 - )", "").title()
                        result["url"] = a
                    case "united states":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_292283 > div > p:nth-child(2) > span > strong").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case "uzbekistan":
                        r = client.get(a.replace("home", "home-based-staff"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_387699 > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > p:nth-child(1) > strong > span > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["position"] = "Ambassador (Concurrently accredited to Kyrgyzstan and Tajikistan)".title()
                        result["url"] = a
                    case "vietnam":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        name = souped2.select_one("#_101_INSTANCE_2TQe_1200230 > div > p:nth-child(11) > span > strong > span").get_text(strip=True, separator=" ")
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                    case _ :
                        result["url"] = a
                        result["position"] = ""

            print("country: {0}; head of mission: {1}".format(result["country"], result["head_of_mission"]))

            tasks.append(result)

            k += 1

    file_name = "{0}_PEP_Malaysia_Diplomatic_Corps.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))

    print(f"Save to {file_name}...")

    try:
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, delimiter=";", fieldnames=("country", "head_of_mission", "position", "url", "photo_link"))
            writer.writeheader()
            writer.writerows(tasks)
            f.close()
        print("Done!!!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
import httpx
import requests
from bs4 import BeautifulSoup
import re
from urllib import parse


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

    response = client.get('https://www.kln.gov.my/overseas/index.php', params=params, headers=headers)
    souped = BeautifulSoup(response.content, "html.parser")
    li_tags = souped.select("ul#why-choose>li")

    k = 0
    tasks = list()
    for li in li_tags:
        country = li.select_one("div.link").get_text(strip=True, separator=" ")
        containers = li.select("ul.submenu>.container:nth-child(1)")
        for container in containers:
            address = container.select_one("ul.submenu>.container:nth-child(1) div>div:nth-child(1) li").get_text(strip=True, separator=" ")
            a = container.select_one("li a").get("href", None)

            space_patterns = re.compile(r"\s{2,}|\xa0{1,}")

            result = {
                    "country": country,
                    "address": space_patterns.sub(" ", address),
                    "head_of_mission": "",
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
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
                        result["url"] = a
                        result["photo_link"] = photo
                    case "austria":
                        r = client.get(a.replace("home", "head_mission"))
                        souped2 = BeautifulSoup(r.content, "html.parser")
                        photo = souped2.select_one("#_101_INSTANCE_2TQe_308035 > div > p:nth-child(1) > img").get("src", "")
                        result['head_of_mission'] = "Ikram Bin Mohammad Ibrahim"
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
                        result['head_of_mission'] = name.title()
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
                        result['head_of_mission'] = space_patterns.sub(" ", name).title()
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
                        result["url"] = a
                    case _ :
                        pass

            print(result)

            tasks.append(result)

            k += 1


if __name__ == "__main__":
    main()
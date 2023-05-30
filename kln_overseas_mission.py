import httpx
from bs4 import BeautifulSoup
import re


client = httpx.Client(verify=False, timeout=5.0)


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
            contacts = container.select_one("ul.submenu>.container:nth-child(1) div>div:nth-child(2) li").get_text(strip=True, separator="\n")

            space_patterns = re.compile(r"\s{2,}")

            # a = container.select_one("li a").get("href", None)

            # if a:
            #     response2 = client.get(a)

            result = {
                "country": country,
                "address": space_patterns.sub(" ", address)
            }

            print(result)

            k += 1


if __name__ == "__main__":
    main()
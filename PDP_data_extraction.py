import os, json, pymongo, threading, time, hashlib
import datetime
from curl_cffi import requests
import pandas as pd
# from sitemap_count_check import my_req
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.longhornsteakhouse.com/menu/flos-filet/prod1580421',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-api-id': '-410612208',
    'x-request-id': 'REQ_1752582876195',
    'x-source-channel': 'WEB',
    # 'cookie': '_gcl_au=1.1.629922285.1752500517; _fbp=fb.1.1752500517881.237277291951598990; _scid=VeKFDh8YVIHAzKdSzNo1VnH3QY4lcVMM; __adroll_fpc=3340688d7a463e78a6c04a24017af9b9-1752500518220; _ScCbts=%5B%5D; _aeaid=b06a87ae-a3bc-41f5-a972-5985ca63fd5a; aelastsite=3kmpGV2u61oUq%2BkWFJyvwEjdjQPxMEs5WSexHzdUHjA7mpyP2Biu9uYxqEFIXd%2BM; aelreadersettings=%7B%22c_big%22%3A0%2C%22rg%22%3A0%2C%22memph%22%3A0%2C%22contrast_setting%22%3A0%2C%22colorshift_setting%22%3A0%2C%22text_size_setting%22%3A0%2C%22space_setting%22%3A0%2C%22font_setting%22%3A0%2C%22k%22%3A0%2C%22k_disable_default%22%3A0%2C%22hlt%22%3A0%2C%22disable_animations%22%3A0%2C%22display_alt_desc%22%3A0%7D; _sctr=1%7C1752431400000; OptanonAlertBoxClosed=2025-07-14T13:42:00.316Z; QuantumMetricUserID=bd1fc7126918c33e2d9c1b036afbcd11; abtestrulesapplied=true; ooreactexp=true; s_nr=1752557552670-Repeat; DRILOCID=2600365; AkSession=b63b401724a00000ee477668c8030000fff80000; PIM-SESSION-ID=ocCLmtTuzXsAFJ52; s_plt=0.76; s_pltp=undefined; ak_bmsc=75045A94478C353145C02C53F16C5418~000000000000000000000000000000~YAAQtjtAFyDNYMmXAQAA2gMJDhxjEGu5gvPnq7XKHm7/DaFJNW6VaBPrT4qSZO127YWv9X/b4lVDlqMwNrnEFdoS+19gvycFad51TgB5e6fYKA/zxn6+qZCWD0sjqKazunJ+DCx0BSZN4KbOeksSfI83C8VP7wJLsSP7l1a19lICJkCkM8EPOBeGknRT8Q+xqrJKd5/OtMXnn30LcnE2PfX2nOuu2G9k2YXxrWbNQdo9L6dZd9O8sA54To0wICNu0kb1viM6J9DSq8DAL0QpRUgvSUKkVW5rLvcLku4e3bqCBz68i5Jk5mHulM115x7tQvKSENFgq4m0Yoj/4+B66nwRWn+kZYeS+HpmTbyO3fWhPnXiZ0GODKJeYcSwztt31d2ZVSbx4N1EAGwoIl+xKUELPsIWbEWph65lfihI2ECYKrbfZyHFt+x5MDkFXqaWrDFaKNB0XKPGMW/hG9HVOnVbn5EZ88A=; AMCVS_13516EE153222FCE0A490D4D%40AdobeOrg=1; AMCV_13516EE153222FCE0A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C20284%7CMCMID%7C13348559101870830000860336538555369186%7CMCAAMLH-1753186929%7C12%7CMCAAMB-1753186929%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1752589329s%7CNONE%7CvVersion%7C5.5.0; s_dslv_s=Less%20than%201%20day; s_vnum=1784036517273%26vn%3D4; s_invisit=true; s_cc=true; at_check=true; QuantumMetricSessionID=c7e6c1106c2f5901e27c9e359a504924; TS01d054ad=010fb72f91904cb9a6d0159ea42e74a8625fccd170b08f9ffc12bfaed2d6b19f5ee7451f7a9d59d3e7765eb81f47b224505c0198b4; _abck=C9519CDC729AA218A736F80705E4296F~0~YAAQtjtAF1cxYcmXAQAAMawNDg4yE7sKv5+VumuW2CJnQkK1En/QrujedtvaoWvL2873UAAIh6w2Xelgv5J6e2xu+9S6CKKd/GGejDKPspLyvKhh3yAcbi+1gA7MvOGgrUS/B0DmhgpSreAYI0BD5O5XHmLZ1pwJgWPqklMMXTlkWnes9q5fS6mWKrzOqGMRkEFosJGPa8iPk9Ae2hhSy8o3m/QhYknaTaf0jYjQzij5lFFyMxtpxKAn6WP4XNcjXRRbQh6f6Y5NqPHvySNOn/CXTxkmFd4niQtYaTSfM+r2QY8lWoms/YdMAEdVi2U10aBDbwG/rLAKcCJI08qPFWJ0hrIe6Pev6rvsIa3RKGFS+vnr1qZL+Tig0VIFQPwQxM791WX4T4hDoRrvpsUGQVhbMmrvF4tMkkkb46At1wq7ZAhr7uwyTOTjVAe1CP0ZEq9rWfgWsOv0cRzPVQq4OjH+23nMNFKEnTZBd8osxoccRLSw5w9r8zMLJoncMELEU6nSRAKFvcVnvpJOGq7SdQZyl4LkPJ08WjuX5lhtBTNtTH2YRF1ytWfKqpSD/hJYCVEZ8L6LOrKX1Aeh96MI7etCddA+SBay4pXkm4rGjRkm71BtIiZVvDTNqLoSiNiFHT5BaII5aUvA~-1~-1~-1; JSESSIONID=xs8OEIaf84IC4IUuxRr2pZuUC2OmB7h1XoITW32UbxeOzX9CYTXq!-206585883; DRIRESTAURANTID=5155; DRIREST=abff6bd0-b730-5204-a127-56d66b40a33f%40%40Prattville%40%4032.460379*-86.403453%40%402295+Cobbs+Ford+Rd%40%40Prattville%40%40AL%40%40360667703%40%403342857630%40%40%7E%40%40%7E%40%40%7E%40%405155; __ar_v4=AZVSC2HB2BBIVH2YQPDPRE%3A20250713%3A29%7COW7HLYTTMRGYVFIPFFVCTJ%3A20250713%3A29; mbox=PC#9d4eafb08bed4b1bbc02e2db80a02116.41_0#1815827614|session#ddc8fc7d50924ea7a8201a30c51c40a0#1752584674; s_gpv=lh%7Cmenu%20flos-filet; s_purl=https%3A%2F%2Fwww.longhornsteakhouse.com%2Fmenu%2Fflos-filet%2Fprod1580421; s_sq=%5B%5BB%5D%5D; s_nr365=1752582866795-Repeat; s_dslv=1752582866797; bm_sz=999DD16151BEE971F37D943A736C4288~YAAQtjtAF0ndYcmXAQAAcloUDhwltPgYxb58qHBT0/3PVmvsvGd7gVP2+X8Hyc8IGRpjS2OWIdPo1laOdND6DMfrT2JJteuMSEMTstEFFUn1/qfxLW8DZ8XUr0jW15F2aU+aivXJLrXgA6uBzp1F7NRyPzJwndQWV644w2IiERx73JRqjEu5715E9ShjocdyeE9LrAvGQwDPOnLXRmsM1bTSk9lIhYJoOAz/fvV/1zhqpSqpk7hNCzB9cpxAUCo9eQ0ST9zNPWClDNZ0ifCPpZSUkzdxV48MX/SEwxWZOfcdBiNzO+Y83qVuVMmpuzDY96hpeCA/31t120Yt4evSap/lDpvKPwnwEyFpF3HwkOvbIjWTNk/cuQCD3s0j+Vjc1TIWEnPXzDiapOZiP/sujJ/SCVAevsaiWGS6B/nvhIzEF7kxrb+4WpvXy/cHnKtfOm+tcOXXCNX5aVcqzdocvYHYvKgdJw==~4599874~3749937; _scid_r=a2KFDh8YVIHAzKdSzNo1VnH3QY4lcVMMh8JCoQ; bm_sv=07A2D3B5BC85AEC485013448A4371CB6~YAAQtjtAF2rfYcmXAQAAUGoUDhy1OwBPO9/Rjf5gt0T6xK2tr6LGxvgNLzkzKMP7Srx4YMFeU2XDsF2VCAjReDKdV7CEsFnGDEjaO6IQ9cP1udkkVhEUcn8IYmHr91yBt0ePHXGz6FhQfwcVeqEALqRRh3nfa/SRm1rQA8iNCOUltoH/JHJ1SNphxq7kfuJjYkXnMoOA9fr8ICI21PGDhHer+rZgW7EjEp5BcOmVEJbJe4/9Lv6SkCofd/ybIK/dfuwlqex5OwEtSie4N9o=~1; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+15+2025+18%3A04%3A36+GMT%2B0530+(India+Standard+Time)&version=202504.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=607e5451-8e03-4e01-bf7a-21ef06fd12d1&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false',
}

results_list = []

#TODO:: Mongo Connection string
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "longhornsteakhouse_US_feasiblity"
COLLECTION_INPUT = "sitemaps_inputs_1"

def process_task(fetch_Product_URL):
    split_fetch_Product_URL = fetch_Product_URL.split("/")[-1]
    url = f"https://www.longhornsteakhouse.com/api/menu/{split_fetch_Product_URL}?locale=en_US&restaurantNum=5155"
    response = requests.get(url=url,  headers=headers, impersonate="chrome120")
    if response.text and response.status_code == 200:
        # TODO::Contain json
        try:
            contains_json = response.text
            if "displayName" in response.text:
                json_contain = json.loads(contains_json)
        except Exception as e:
            print(e)


        #URL
        try:
            URL = fetch_Product_URL
        except:...

        #Category
        try:
            Category = json_contain.get("product").get('keywords')[-1]
        except:Category = ""

        #MenuItemName
        try:
            MenuItemName = json_contain.get("product").get('displayName')
        except:...

        #SubCategory
        try:
            SubCategory = json_contain.get("product").get('keywords')[-2]
        except:SubCategory = ""

        #Flavor
        try:
            Flavor = ""
        except:...

        #Brand_StoreID requeset ......
        headers_2 = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=1, i',
            # 'referer': 'https://www.longhornsteakhouse.com/menu/flos-filet/prod1580421',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-api-id': '1990306551',
            'x-request-id': 'REQ_1752582874591',
            'x-source-channel': 'WEB',
            # 'cookie': '_gcl_au=1.1.629922285.1752500517; _fbp=fb.1.1752500517881.237277291951598990; _scid=VeKFDh8YVIHAzKdSzNo1VnH3QY4lcVMM; __adroll_fpc=3340688d7a463e78a6c04a24017af9b9-1752500518220; _ScCbts=%5B%5D; _aeaid=b06a87ae-a3bc-41f5-a972-5985ca63fd5a; aelastsite=3kmpGV2u61oUq%2BkWFJyvwEjdjQPxMEs5WSexHzdUHjA7mpyP2Biu9uYxqEFIXd%2BM; aelreadersettings=%7B%22c_big%22%3A0%2C%22rg%22%3A0%2C%22memph%22%3A0%2C%22contrast_setting%22%3A0%2C%22colorshift_setting%22%3A0%2C%22text_size_setting%22%3A0%2C%22space_setting%22%3A0%2C%22font_setting%22%3A0%2C%22k%22%3A0%2C%22k_disable_default%22%3A0%2C%22hlt%22%3A0%2C%22disable_animations%22%3A0%2C%22display_alt_desc%22%3A0%7D; _sctr=1%7C1752431400000; OptanonAlertBoxClosed=2025-07-14T13:42:00.316Z; QuantumMetricUserID=bd1fc7126918c33e2d9c1b036afbcd11; abtestrulesapplied=true; ooreactexp=true; s_nr=1752557552670-Repeat; DRILOCID=2600365; AkSession=b63b401724a00000ee477668c8030000fff80000; PIM-SESSION-ID=ocCLmtTuzXsAFJ52; s_plt=0.76; s_pltp=undefined; ak_bmsc=75045A94478C353145C02C53F16C5418~000000000000000000000000000000~YAAQtjtAFyDNYMmXAQAA2gMJDhxjEGu5gvPnq7XKHm7/DaFJNW6VaBPrT4qSZO127YWv9X/b4lVDlqMwNrnEFdoS+19gvycFad51TgB5e6fYKA/zxn6+qZCWD0sjqKazunJ+DCx0BSZN4KbOeksSfI83C8VP7wJLsSP7l1a19lICJkCkM8EPOBeGknRT8Q+xqrJKd5/OtMXnn30LcnE2PfX2nOuu2G9k2YXxrWbNQdo9L6dZd9O8sA54To0wICNu0kb1viM6J9DSq8DAL0QpRUgvSUKkVW5rLvcLku4e3bqCBz68i5Jk5mHulM115x7tQvKSENFgq4m0Yoj/4+B66nwRWn+kZYeS+HpmTbyO3fWhPnXiZ0GODKJeYcSwztt31d2ZVSbx4N1EAGwoIl+xKUELPsIWbEWph65lfihI2ECYKrbfZyHFt+x5MDkFXqaWrDFaKNB0XKPGMW/hG9HVOnVbn5EZ88A=; AMCVS_13516EE153222FCE0A490D4D%40AdobeOrg=1; AMCV_13516EE153222FCE0A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C20284%7CMCMID%7C13348559101870830000860336538555369186%7CMCAAMLH-1753186929%7C12%7CMCAAMB-1753186929%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1752589329s%7CNONE%7CvVersion%7C5.5.0; s_dslv_s=Less%20than%201%20day; s_vnum=1784036517273%26vn%3D4; s_invisit=true; s_cc=true; at_check=true; QuantumMetricSessionID=c7e6c1106c2f5901e27c9e359a504924; TS01d054ad=010fb72f91904cb9a6d0159ea42e74a8625fccd170b08f9ffc12bfaed2d6b19f5ee7451f7a9d59d3e7765eb81f47b224505c0198b4; _abck=C9519CDC729AA218A736F80705E4296F~0~YAAQtjtAF1cxYcmXAQAAMawNDg4yE7sKv5+VumuW2CJnQkK1En/QrujedtvaoWvL2873UAAIh6w2Xelgv5J6e2xu+9S6CKKd/GGejDKPspLyvKhh3yAcbi+1gA7MvOGgrUS/B0DmhgpSreAYI0BD5O5XHmLZ1pwJgWPqklMMXTlkWnes9q5fS6mWKrzOqGMRkEFosJGPa8iPk9Ae2hhSy8o3m/QhYknaTaf0jYjQzij5lFFyMxtpxKAn6WP4XNcjXRRbQh6f6Y5NqPHvySNOn/CXTxkmFd4niQtYaTSfM+r2QY8lWoms/YdMAEdVi2U10aBDbwG/rLAKcCJI08qPFWJ0hrIe6Pev6rvsIa3RKGFS+vnr1qZL+Tig0VIFQPwQxM791WX4T4hDoRrvpsUGQVhbMmrvF4tMkkkb46At1wq7ZAhr7uwyTOTjVAe1CP0ZEq9rWfgWsOv0cRzPVQq4OjH+23nMNFKEnTZBd8osxoccRLSw5w9r8zMLJoncMELEU6nSRAKFvcVnvpJOGq7SdQZyl4LkPJ08WjuX5lhtBTNtTH2YRF1ytWfKqpSD/hJYCVEZ8L6LOrKX1Aeh96MI7etCddA+SBay4pXkm4rGjRkm71BtIiZVvDTNqLoSiNiFHT5BaII5aUvA~-1~-1~-1; JSESSIONID=xs8OEIaf84IC4IUuxRr2pZuUC2OmB7h1XoITW32UbxeOzX9CYTXq!-206585883; DRIRESTAURANTID=5155; DRIREST=abff6bd0-b730-5204-a127-56d66b40a33f%40%40Prattville%40%4032.460379*-86.403453%40%402295+Cobbs+Ford+Rd%40%40Prattville%40%40AL%40%40360667703%40%403342857630%40%40%7E%40%40%7E%40%40%7E%40%405155; _scid_r=amKFDh8YVIHAzKdSzNo1VnH3QY4lcVMMh8JCoA; __ar_v4=AZVSC2HB2BBIVH2YQPDPRE%3A20250713%3A29%7COW7HLYTTMRGYVFIPFFVCTJ%3A20250713%3A29; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+15+2025+18%3A03%3A33+GMT%2B0530+(India+Standard+Time)&version=202504.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=607e5451-8e03-4e01-bf7a-21ef06fd12d1&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false; mbox=PC#9d4eafb08bed4b1bbc02e2db80a02116.41_0#1815827614|session#ddc8fc7d50924ea7a8201a30c51c40a0#1752584674; s_gpv=lh%7Cmenu%20flos-filet; s_purl=https%3A%2F%2Fwww.longhornsteakhouse.com%2Fmenu%2Fflos-filet%2Fprod1580421; s_sq=%5B%5BB%5D%5D; s_nr365=1752582866795-Repeat; s_dslv=1752582866797; bm_sz=999DD16151BEE971F37D943A736C4288~YAAQtjtAF0ndYcmXAQAAcloUDhwltPgYxb58qHBT0/3PVmvsvGd7gVP2+X8Hyc8IGRpjS2OWIdPo1laOdND6DMfrT2JJteuMSEMTstEFFUn1/qfxLW8DZ8XUr0jW15F2aU+aivXJLrXgA6uBzp1F7NRyPzJwndQWV644w2IiERx73JRqjEu5715E9ShjocdyeE9LrAvGQwDPOnLXRmsM1bTSk9lIhYJoOAz/fvV/1zhqpSqpk7hNCzB9cpxAUCo9eQ0ST9zNPWClDNZ0ifCPpZSUkzdxV48MX/SEwxWZOfcdBiNzO+Y83qVuVMmpuzDY96hpeCA/31t120Yt4evSap/lDpvKPwnwEyFpF3HwkOvbIjWTNk/cuQCD3s0j+Vjc1TIWEnPXzDiapOZiP/sujJ/SCVAevsaiWGS6B/nvhIzEF7kxrb+4WpvXy/cHnKtfOm+tcOXXCNX5aVcqzdocvYHYvKgdJw==~4599874~3749937; bm_sv=07A2D3B5BC85AEC485013448A4371CB6~YAAQtjtAF4neYcmXAQAA+2MUDhylGm+n2qqM8Jqvqay+Z4Csnu0fDbEdpYzV0+HcwRsDUnhOjAXb8wGpXAMx+1lK6cfoiGp+tpkidxOBCtRf6bdU2UZP+vtzsxClqrDzKbxNP3e0Vf3/Mx3pEkfIoZijChq/Njl+AYoqhf+GuSA0beZgqnBM8Npqt3zhHlxlueYM5+R8lORJNF2XUuP5WbQsABcHlTzZrI6gRNf9HfbMR5YM7V7zI7hmzk0bry1WmUC8umYCaO8WGeRQz3U=~1',
        }

        response2 = requests.get(
            'https://www.longhornsteakhouse.com/api/restaurants/5155?locale=en_US&restaurantNumber=5155',
            headers=headers_2,
            impersonate="chrome120"
        )

        my_res2 = response2.json()

        check_address1_street1 = my_res2.get("restaurant").get("contactDetail").get("address").get("street1")
        check_address1_city = my_res2.get("restaurant").get("contactDetail").get("address").get("city")
        check_address1_stateCode = my_res2.get("restaurant").get("contactDetail").get("address").get("stateCode")
        check_address1_zipCode = my_res2.get("restaurant").get("contactDetail").get("address").get("zipCode")
        new_check_address1_zipCode = str(check_address1_zipCode)[:5]

        main_address = f"{check_address1_street1} {check_address1_city},{check_address1_stateCode} {new_check_address1_zipCode}"

        #Brand_StoreID
        try:
            Brand_StoreID = my_res2.get("restaurant").get("restaurantNumber")
        except:...

        #Address
        try:
            Address = main_address
        except:...

        #City
        try:
            City = check_address1_city
        except:...

        #State
        try:
            State = my_res2.get("restaurant").get("contactDetail").get("address").get("stateName")
        except:...

        #ZipCode
        try:
            ZipCode = new_check_address1_zipCode
        except:...

        #Country
        try:
            Country = my_res2.get("restaurant").get("contactDetail").get("address").get("country")
        except:...

        #Latitude
        try:
            Latitude = my_res2.get("restaurant").get("contactDetail").get("address").get("coordinates").get("latitude")
        except:...

        #Longitude
        try:
            Longitude = my_res2.get("restaurant").get("contactDetail").get("address").get("coordinates").get("longitude")
        except:...


        #ExtractionDate
        try:
            ExtractionDate = datetime.datetime.now().strftime("%Y-%m-%d")
        except:...


        sub_checking_json = json_contain.get("product").get("skus")
        for sub_checking_json_i in sub_checking_json:
            item = {}

            item['URL'] = URL
            item['Category'] = Category.upper() if Category else ""
            item['SubCategory'] = SubCategory.upper() if SubCategory else ""
            item['MenuItemName'] = MenuItemName

            # MenuItemID
            try:
                item['MenuItemID'] = sub_checking_json_i.get("id")
            except:...

            #LongName
            try:
                item['LongName'] = sub_checking_json_i.get('displayName')
            except:...

            #Price
            try:
                item['Price'] = sub_checking_json_i.get("price").get("value")
            except:...

            item['Flavor'] = Flavor

            # Size
            try:
                import re
                try:
                    pack_size_pattern = re.compile(r'(\d+\.?\d*)\s*(ml|l|kg|gm|g|mg|pound|lb|oz)', re.IGNORECASE)
                    product_name_size = sub_checking_json_i.get('displayName')
                    product_pack_size_check = pack_size_pattern.search(product_name_size)
                    product_pack_size_once = product_pack_size_check.group()
                except:
                    product_pack_size_once = ""

                item['Size'] = product_pack_size_once
            except:...

            item['Brand_StoreID'] = Brand_StoreID
            item['Address'] = Address
            item['City'] = City
            item['State'] = State
            item['ZipCode'] = ZipCode
            item['Country'] = Country
            item['Latitude'] = Latitude
            item['Longitude'] = Longitude
            item['ExtractionDate'] = ExtractionDate


            results_list.append(item)
            print("Done")


MAX_THREADS = 20
def main():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection_ip = db[COLLECTION_INPUT]
    # pending_tasks = list(collection_ip.find({"url": "https://www.longhornsteakhouse.com/menu/cabernet-sauvignon/prod1580479"}))
    # pending_tasks = list(collection_ip.find({"status": "Pending"}))
    pending_tasks = list(collection_ip.find({}))

    if not pending_tasks:
        print("No pending tasks found.")
        return

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for task in pending_tasks:
            url = task.get("url", "")
            future = executor.submit(process_task, url)
            futures.append(future)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing task: {e}")

    print("All tasks completed.")

if __name__ == '__main__':
    main()

print(results_list)
df = pd.DataFrame(results_list)

# Export to Excel
output_path = "longhornsteakhouse_sample_22072025.xlsx"
df.to_excel(output_path, index=False)

print(f"Excel file saved to {output_path}")

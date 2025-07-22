import re, hashlib
from curl_cffi import requests
from pathlib import Path
from pymongo import MongoClient


all_urls = []

from itertools import product
# #TODO:: Mongo Connection string
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["longhornsteakhouse_US_feasiblity"]
collection_ip = db["sitemaps_inputs_1"]

from curl_cffi import requests

url = "https://www.longhornsteakhouse.com/api/menu?locale=en_US&restaurantNum=5155"

payload = {}
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
  'customtimeout': '20000',
  'priority': 'u=1, i',
  # 'referer': 'https://www.longhornsteakhouse.com/menu/drinks/signature-cocktails',
  'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
  'x-api-id': '1871875427',
  'x-concept-code': 'LH',
  'x-request-id': 'REQ_1753173025731',
  'x-source-channel': 'WEB',
  'Cookie': 'mbox=session#17631980f20c462283021c66bee1ffbd#1753174814|PC#17631980f20c462283021c66bee1ffbd.41_0#1816417754; PIM-SESSION-ID=EiP07dWjVqzt9UIc; QuantumMetricSessionID=7a1fcdfd2ce067abab402f198aa913c0; AkSession=ac24c31754a90000024c7f684e020000398d0500; abtestrulesapplied=true; ooreactexp=true; ak_bmsc=A79F0251782C1B67CD29468124CD4F5F~000000000000000000000000000000~YAAQrCTDF/zRAhuYAQAAHupAMRwtb15LRZg50raUrm26txJlgjhNNXXW1Cy76IHioZgfp6WWYDDDFhi8SEHUKp0x1zofezySCMWPC5brOszx2rrLedZiJyzES++V7USzpmc6HbB/RmkMRaqAgmrIVb2lL7McySINsmdcHCRWeg1ASav0GBHaDyFoeCPjeWDdlzTMGl85TkbL0LjHkGdgtwxwjrAqnwnWqmh1vTNVVWDPF5uc6ZzwQVqfWTSX9zvE9RUgbWmXIiTBbf/HkweNZI6l2XqQjHfADV7Q87X9X7HbqLSty4yBOdCyuGhY15H/EA+3SalNu8vbLA3/ac00Sajfsy1JBABtQQ1CVP2Uk4tsBa2xs5IFUCENYCWmyk2sRj/oTbQ+T3iEMipB3/It4/k4QQ45xg==; bm_sz=0704FB45AE150016E460FAF13A951C2E~YAAQrCTDFwnTAhuYAQAAAPBAMRwwXW3bgFiZJ5qgas4k3gqTrtMUNZnyvBtkgRTWJgmaprjVYxqZGI5ikbT3j9tXQ1MTcK74Sn6A45cED74Qcot6IIWXXDIwUgaG21SPI9oCCvELkpHm3GDh669lTIKot7/b8aAj5ZrVSCCVCpLzaxxzA2ESKR0Ra6VZInmNoF/sgc2OaBmMFvfRUlNwFq8q4AtWHOcT9Hp+fZgNLdQrz/bLCj+2I00sm9MOMju9zWKCRLvuswTi3DztWtoUJbDu6jAqwYnXk49+v4dTQO89sRsRaMnRDpbY18SJk//Efp3+xNpTZnQspjW1iAnUuEw6Ci6SevE/r7yexda4IK2Na23WILCthrFk+27AzPqxX+NZ8pqMCyIn9YMu0+kgkM3qr0Hf9dI+IJ1hDwA0251OpSIbBtUeOuFkBb/9ty9De01RGmHIvrk=~3356994~4404019; s_plt=2.90; s_pltp=undefined; AMCVS_13516EE153222FCE0A490D4D%40AdobeOrg=1; AMCV_13516EE153222FCE0A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C20292%7CMCMID%7C85068296633432911041590825051491705020%7CMCAAMLH-1753777799%7C7%7CMCAAMB-1753777799%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1753180199s%7CNONE%7CvVersion%7C5.5.0; _gcl_au=1.1.1634166162.1753173000; _scid=ZU-3vfJptquPjKRUw2LMVGHUcz0w1YuujlrZlg; _scid_r=ZU-3vfJptquPjKRUw2LMVGHUcz0w1YuujlrZlg; _fbp=fb.1.1753173000439.901519054461771804; s_gpv=lh%7Cmenu%20drinks; s_purl=https%3A%2F%2Fwww.longhornsteakhouse.com%2Fmenu%2Fdrinks%2Fsignature-cocktails; s_vnum=1784709000505%26vn%3D1; s_invisit=true; s_cc=true; __adroll_fpc=326339663dbcd250da97b11d055d335c-1753173000771; __ar_v4=AZVSC2HB2BBIVH2YQPDPRE%3A20250721%3A5%7COW7HLYTTMRGYVFIPFFVCTJ%3A20250721%3A5; _aeaid=6ac442bd-a484-4395-b101-3ed236fdcc42; aelastsite=3kmpGV2u61oUq%2BkWFJyvwEjdjQPxMEs5WSexHzdUHjA7mpyP2Biu9uYxqEFIXd%2BM; aelreadersettings=%7B%22c_big%22%3A0%2C%22rg%22%3A0%2C%22memph%22%3A0%2C%22contrast_setting%22%3A0%2C%22colorshift_setting%22%3A0%2C%22text_size_setting%22%3A0%2C%22space_setting%22%3A0%2C%22font_setting%22%3A0%2C%22k%22%3A0%2C%22k_disable_default%22%3A0%2C%22hlt%22%3A0%2C%22disable_animations%22%3A0%2C%22display_alt_desc%22%3A0%7D; cebs=1; _ce.clock_data=2863%2C209.87.169.106%2C1%2C7ddeda88d0c599cc494da0dece6554d5%2CChrome%2CUS; cebsp_=13; _ce.s=lcw~1753173003099~v11ls~1049c570-66d6-11f0-9a4d-99f86a67ef52~v~f1c370ccb590f8f9b85379a7b4b0b9fd7a424419~vir~new~lva~1753173001936~vpv~0~v11.cs~204127~v11.s~1049c570-66d6-11f0-9a4d-99f86a67ef52~v11.vs~f1c370ccb590f8f9b85379a7b4b0b9fd7a424419~v11.fsvd~eyJ1cmwiOiJsb25naG9ybnN0ZWFraG91c2UuY29tL21lbnUvZHJpbmtzL3NpZ25hdHVyZS1jb2NrdGFpbHMiLCJyZWYiOiIiLCJ1dG0iOltdfQ%3D%3D~v11.sla~1753173003088~v11.ss~1753173003098~lcw~1753173003103; OptanonAlertBoxClosed=2025-07-22T08:30:04.826Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+22+2025+14%3A00%3A04+GMT%2B0530+(India+Standard+Time)&version=202504.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=fd7d04dd-083b-4b34-85a3-3e9d05f1b81f&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false; _abck=001CE85F6E7BFCF0F2F860C3F7E9952E~0~YAAQrCTDFxrYAhuYAQAAXgdBMQ6c9hMXyiiG4juvKSbGtXrfvfiUEJe5DIIEblpOwgC5H/nakoZuNIOPaN6EhG2e63XBvG2Ck1KoOUz9+zxLChUwSjW/qcntsVVIEDURZNWjgBkPNa/QWW4H4OXFyDyjcXgJbdJSARidAkWZ1vCE40Sys/KbM3rBTpUXOGrvpRztMBrDebJoZuOQ8njQH4ROUHB2AiGCtzzhWth+8jZYp9suqIS5dv8+oiW8c0mWckKO/UZcAYoGwKRKfI5SB3tCOHbLracMeYdH6VzEcknmylXuNbDxdB6jC1x5u92BZKV0X1ou/UY8FBFfQd1yW2t99LsEGcy+OqLPqT47CypHlotE1UDkwIWq8oigq2TozxZswTWVjumad7PTHp7Tl5TjAJ2hKjQ33/QWYFstGuZEKCnh2W5balUYdMakfOGEwIOM0teSuVtBEAI6ZyhhnqNFNsdkIFMibN4F7Lj41nSqzkJ98zM8TjApwkaxy/biprpHhPg52afSRS6NfdTckmMLYVCLRQtEgo+00zV88XFfRpdD~-1~||0||~-1; _ScCbts=%5B%5D; _sctr=1%7C1753122600000; DRIRESTAURANTID=5642; DRIREST=790a1b88-826f-5b75-8b1d-2e7771cf3ae9%40%40Trussville%40%4033.64086*-86.62409%40%405957+Chalkville+Mountain+Lane%40%40Birmingham%40%40AL%40%40352353318%40%402056618070%40%40%7E%40%40%7E%40%40%7E%40%405642; s_nr365=1753173024028-New; s_dslv=1753173024030; s_sq=%5B%5BB%5D%5D; bm_sv=45B509A739755F2F10BF7321304E513F~YAAQrCTDFxbrAhuYAQAAVVhBMRwXHprdLX7iSmxP0aSbxvYLXPv4Izy/H8XIVPEq4iUwls5Egyoon1DlbmIuw5/gYdQcv9gs9bLUmcy6kHVgSoz6/C4jDH+v1U9FR6hE7EkDPFAqyt8XCn/sbvtfgJARwLRC2PlMemd8ubE64P1HedS09EE8IVxujJsTmMP7P0ZvbDgem9lJQV26eOiqmU9IpcUXaZqkJqUXaI9JdHns+/R+sw6X+deAltcG8paw+bUzjMXBEPw9nmhI5w==~1; _abck=001CE85F6E7BFCF0F2F860C3F7E9952E~-1~YAAQxTtAF9MZhxSYAQAAnVtEMQ7uv11sZvAsCTGmxDCUN7m6rO9rcA77UPNOgehZyo3M5BBvxtV7aJOOI8aKEFmm/sfWI/kRmfFI7fOg9FKFQMBaf1vTjANXWdCg2tZ+jxul+z/3BYNhl/q1DNZzMVa956/JBuoKcTi6TLhVIYFA7OVa+5GETdOFMMhgE+xA6H0eDM7nBoS66549USEhjmKXGHPz/x1TiMX9aCqMXwSq8kYiPE2VxCaWPsjzkK59lpGLfsb7FTRl+qUZYnUKSaMldXv1CDhAesB7ulqyH9TVMnqG1FU2O5HmUrmjTy1t/By2HBbteGXS9XCr4IwVY+PZ88rFD1ZgvrB0qNdKKPEQy3cTt5ArJ/52hiGU4qbn5HaMG8sadiw6+wcX/MF9FM8oon7qf/YPh3l1Fh35VJ5v5HaJDZmZxSKP7pB4TsyIZjRJBAxy+gY+3XbQH4SSHIY13xWUUWraX6ezei8+qLzoHZ3yqjcmNYbjDgm/TK3NxrEuxQrmv9VhdCzuUrB1jlM15IvHgueNUfna+fYXRhZOJk5y~0~-1~-1; bm_sv=45B509A739755F2F10BF7321304E513F~YAAQxTtAF9QZhxSYAQAAnVtEMRx1NsdJFiMJ7ep+xABK9Fuf0rKAlD0mRU5vwtBVLY8cyYT0eSOApP2y2uJ7MPCFOY1qcCFakCgErbsMJhBfLDIIyk1I1p6uPtqwAx94x/qOnDpkmPp1KJgZ43Cpa0AlSu5l9wLeNLsMbZ+oc+OGYxQHkHoUbxLmj0zItFLeNuaiYGxboZySZCo50L0rqR6oWbcs98virvC8o6Vi6LGq/J/BN9dhNLXVgvTCdrwvHMS58sDRL6O63FceaQ==~1'
}

response = requests.request("GET",
                            url,
                            headers=headers,
                            data=payload,
                            impersonate="chrome120"
                            )

contains_cateogory_json = response.json()

main_category = contains_cateogory_json.get("categories")

for sub_cateogries in main_category:

    # print(sub_cateogries)
    try:
        sub_cate = sub_cateogries.get("subCategories")
        if sub_cate:
            for cate in sub_cate:
                sub_cate1 = cate.get("products")
                for products_list in sub_cate1:
                    product_id = products_list.get("id")
                    product_slug = products_list.get("slug")

                    final_url = f"https://www.longhornsteakhouse.com/menu/{product_slug}/{product_id}"
                    print(final_url)
                    all_urls.append(final_url)
        else:
            sub_cate = sub_cateogries.get("products")
            for products_list in sub_cate:
                product_id = products_list.get("id")
                product_slug = products_list.get("slug")

                final_url = f"https://www.longhornsteakhouse.com/menu/{product_slug}/{product_id}"
                print(final_url)
                all_urls.append(final_url)

    except:...


for url in all_urls:
    item = {}
    # TODO:: unique hashid
    try:
        unique_string = f"{url}"
        hashed_id = hashlib.sha256(unique_string.encode()).hexdigest()
        item['_id'] = hashed_id
        item['url'] = url
        item['status'] = "Pending"
    except Exception as e:
        print(e)

    # TODO:: Insert the item
    try:
        # collection_ip.insert_one(item)
        print("Item inserted successfully!")
    except Exception as e:
        print(f"Error: {e}")

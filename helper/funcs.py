import requests,re,bs4,warnings,json

warnings.filterwarnings('ignore')

def get_animes(query) -> dict :
    """
    return a dict of urls and imgs and titles
    example: {'name of anime':{'img':'img of anime','url':'url of anime'}}
    :param query:
    :return:
    """
    headers = {
        'authority': 'animelek.me',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,ar;q=0.9,en-US;q=0.8,uz;q=0.7',
        # 'cookie': '_gid=GA1.2.1616766172.1692215043; _popfired_expires=Invalid%20Date; _gat_gtag_UA_169345539_1=1; _ga_96MJGWFBKW=GS1.1.1692217540.2.1.1692217542.58.0.0; _ga=GA1.1.409224257.1692215043; _popfired=3; lastOpenAt_=1692217547376',
        'referer': 'https://animelek.me/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    params = {
        's': query,
    }
    response = requests.get('https://animelek.me/search/', params=params, headers=headers)
    b = bs4.BeautifulSoup(response.content, 'html.parser')
    lists = b.find('div', attrs={'class': 'row display-flex'}).find_all('div', attrs={'class': 'play-button-extra'})
    results = {}
    for anime in lists:
        tt = anime.find_next('a', attrs={'class': 'overlay'}).get('href')
        full = re.match('https://animelek\.me/anime/(.*?)$', tt)
        results[full.group(1).replace('-', ' ').replace('/', '')] = {'url': tt}
    return results

def check_anime(url) -> dict :
    """
    return a dict of information about the anime like descreption and title
    example: {'desc:':'infos','title':'title of the anime'}
    :param url:
    :return:
    """
    headers = {
        'authority': 'animelek.me',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,ar;q=0.9,en-US;q=0.8,uz;q=0.7',
        # 'cookie': '_gid=GA1.2.1616766172.1692215043; _popfired_expires=Invalid%20Date; _ga_96MJGWFBKW=GS1.1.1692217540.2.1.1692217555.45.0.0; _ga=GA1.1.409224257.1692215043; _popfired=4; lastOpenAt_=1692217753046',
        'referer': 'https://animelek.me/search/?s=naruto',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    b = bs4.BeautifulSoup(response.content, 'html.parser')
    to = b.find('div', attrs={'class': 'col-sm-3'})
    kind = to.find_all('small')[1].text
    to2 = b.find('div', attrs={'class': 'col-sm-9'}).find('p', attrs={'class': 'anime-story'}).text
    kind = "انمي/حلقات متعددة" if kind == "TV" else "فلم/حلقة واحده"
    results = {'desc':to2,'kind':kind}
    return results

def get_espodes(url,limit = 12) -> dict :
    """
    return a dictionary of espodies titles & urls
    Note: The defulte limit is 12 you can change it by pass limit param
    example: {'name of anime':'url of anime'}
    :param url:
    :return:
    """
    headers = {
        'authority': 'animelek.me',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,ar;q=0.9,en-US;q=0.8,uz;q=0.7',
        # 'cookie': '_gid=GA1.2.1616766172.1692215043; _popfired_expires=Invalid%20Date; _ga_96MJGWFBKW=GS1.1.1692217540.2.1.1692217555.45.0.0; _ga=GA1.1.409224257.1692215043; _popfired=4; lastOpenAt_=1692217753046',
        'referer': 'https://animelek.me/search/?s=naruto',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    b = bs4.BeautifulSoup(response.content, 'html.parser')
    to = b.find('div', attrs={'class': 'row display-flex', 'id': 'DivEpisodesList'})
    to2 = to.find_all('div', attrs={'class': 'hover'})
    results = {}
    for esp in to2:
        if len(results) == limit:
            break
        results[esp.find_next('img').get('alt')] = esp.find_next('a', attrs={'class': 'overlay'}).get('href')
    return results

def get_select_esp(url:str,num:int) -> list:
    """
    return a dictionary of espodies titles & urls
    Note: The defulte limit is 12 you can change it by pass limit param
    example: {'name of anime':'url of anime'}
    :param url:
    :return:
    """
    headers = {
        'authority': 'animelek.me',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,ar;q=0.9,en-US;q=0.8,uz;q=0.7',
        # 'cookie': '_gid=GA1.2.1616766172.1692215043; _popfired_expires=Invalid%20Date; _ga_96MJGWFBKW=GS1.1.1692217540.2.1.1692217555.45.0.0; _ga=GA1.1.409224257.1692215043; _popfired=4; lastOpenAt_=1692217753046',
        'referer': 'https://animelek.me/search/?s=naruto',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    b = bs4.BeautifulSoup(response.content, 'html.parser')
    to = b.find('div', attrs={'class': 'row display-flex', 'id': 'DivEpisodesList'})
    to2 = to.find_all('div', attrs={'class': 'hover'})
    results = [f"{to2[num - 1].find_next('img').get('alt')}",f"{to2[num - 1].find_next('a', attrs={'class': 'overlay'}).get('href')}"]
    return results

def get_espode_dl_links(url) -> dict :
    """
    This function sometimes can't parse the anime mp4 because the capatcha bypassing
    :param url:
    :return:
    """
    headers = {
        'authority': 'animelek.me',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,ar;q=0.9,en-US;q=0.8,uz;q=0.7',
        # 'cookie': '_gid=GA1.2.1616766172.1692215043; _popfired_expires=Invalid%20Date; _ga_96MJGWFBKW=GS1.1.1692217540.2.1.1692218124.58.0.0; _ga=GA1.1.409224257.1692215043; _popfired=6; lastOpenAt_=1692218756569',
        'referer': 'https://animelek.me/anime/naruto/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    response = requests.get(
        url,
        headers=headers,
    )
    results = {}
    bs = bs4.BeautifulSoup(response.content, 'html.parser')
    pparser = re.findall('<a data-ep-url="(.*?)" id="(.*?)"', str(bs))
    for i in pparser:
        results[i[1]] = i[0]
    return results

def mp4upload(url:str,filename:str) -> bool or int:
    full = re.match('https://www\.mp4upload\.com/embed-(.*?)\.html$',url)
    headers = {
        'authority': 'www.mp4upload.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,ar;q=0.9,en-US;q=0.8,uz;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'lang=english; affiliate=qM6EesT9M0gprG3OHA1JRdnZTY%2FuKWOTQDxzb%2BmkczKaZ9gkkMKvztf1AE49%2B7Nwab4UF%2FWD%2FFSgViLdYPj%2FyXESqM%2BS00vAwfpz%2Fmhq8PhO%2B5x%2FhV%2FRzO6glf83wrQ%3D',
        'origin': 'https://www.mp4upload.com',
        'referer': f'https://www.mp4upload.com/{full.group(1)}',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    data = {
        'op': 'download2',
        'id': full.group(1),
        'rand': '',
        'referer': 'https://animelek.me/',
        'method_free': 'Free Download',
        'method_premium': '',
    }
    try:
        response = requests.post(f"https://www.mp4upload.com/{full.group(1)}", headers=headers, data=data, allow_redirects=True,
                          )
        if '<!doctype' in response.text:
            return 404
        else:
            open(filename, 'wb').write(response.content)
            return True
    except:
        return False

def google_drive(url:str,filename:str) -> bool or int:
    full = re.match('https://drive\.google\.com/file/d/(.*?)/preview$',url)
    #https://drive.google.com/file/d/10G82kTIQUWKE2f5LYmCHqY8lNZbncHOC/preview
    headers = {
        'authority': 'drive.google.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,ar;q=0.9,en-US;q=0.8,uz;q=0.7',
        'cache-control': 'max-age=0',
        # 'content-length': '0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '__Secure-ENID=12.SE=En6Mq90ocAPcR0QEa8GpL0lnEJJpZRfmvVwR4hkM2_E8Zc3YI-ERfGSd08kyY5VFopZCqGut0GaScqYdrkxyHf8dwR-7AvHjChWGP3jV7Td9Xf_rMXtIqPg8LLctQpP_vySQXGfXn0cH4N4Cp-IuEeXJHzf2J1RlDYIy4Czo3s4HO7FCTeGFcbDazfs1HDUqc1V1j_jV7zDkpoG5M9dp3VYlPxr-8YXYdUb6ccVI_Fk_dpoqRRZuWojjZSJAWNasdICuYn3X4x7ZGmgu; SID=ZghXbif6Ee3Zi1nA2MhuyCa7c1oHwaQzRBziVg0dszqaQnfQ1owJsw5rhGAhCADoPUYvLQ.; __Secure-1PSID=ZghXbif6Ee3Zi1nA2MhuyCa7c1oHwaQzRBziVg0dszqaQnfQPOyHz18iWoX0AFz_lRH51Q.; __Secure-3PSID=ZghXbif6Ee3Zi1nA2MhuyCa7c1oHwaQzRBziVg0dszqaQnfQjh7037qnHtgAHOtKKTZ-3w.; HSID=AveqyK2yyPw3iVk6y; SSID=AhbouT1BICtONwOFp; APISID=VnCbBJJdvJl8mziZ/AQto-LR0JRI-i47pI; SAPISID=jLxzC1vmtHzFbZdj/AfZ1lfCdkwhp7oVgF; __Secure-1PAPISID=jLxzC1vmtHzFbZdj/AfZ1lfCdkwhp7oVgF; __Secure-3PAPISID=jLxzC1vmtHzFbZdj/AfZ1lfCdkwhp7oVgF; SEARCH_SAMESITE=CgQI-5gB; AEC=Ad49MVHTZYM8TsP9OE1krchCUPbGy-mOtCzHHXzswkMZev9UiKo9R5O-8g; NID=511=EZZ3-8KLS3Gc-N8eAP-S2bUREc-Eq_ukoSiIgFNEQ-MkhzmUJAYFlt2Gt8w1tMbnRbnnfRargm-Z17C-8WykbYMr_RS4ZvAG9HvIIKwgllVmP8bQGxMCZ4nFLvj7JGJmskoiZNvsd1kbSPLPdjWw9ERIQfPMG7jwWWMEAKH6eq6fBrhg1TD3Nd8AHKwd2h8OAp_2FcgW2UzUqEgFIW0MHSPjmsKfDJSeR_bqeg6YGXp0sPjO5kRklgB27Gh_FCY-zIW2VkZ5Nj5z8E3cXnK4nUKd6pAN6oSKG8o9UZp-5q6cg-9U3JalremsjWFZR7v9SZHMd7OFRGX5lDp5DFyq3JEOiYvj_i90cVIGAG7JI-D9Q1BzUDSiSJGmwgonZj87C7wQoHKsyy0CK-2m0AIzTn8fmOVMyw; OSID=ZwhXbtWqrA0UP3mZYsVBNPHaZSSrpHGW2ho86QR6yrN4DZYyqaXTn_iyCmqedIjHpjWITg.; __Secure-OSID=ZwhXbtWqrA0UP3mZYsVBNPHaZSSrpHGW2ho86QR6yrN4DZYy17y8jKYAB5iOW7LoDsW4Ng.; DRIVE_STREAM=InjwOr3DNyQ; 1P_JAR=2023-08-16-20; __Secure-1PSIDTS=sidts-CjEBSAxbGYXzkoOAsdV5h4Ss7IAqFX-FiXy-L-IeGZRvUR4W4g6zufe-R9kOghXQ7x0IEAA; __Secure-3PSIDTS=sidts-CjEBSAxbGYXzkoOAsdV5h4Ss7IAqFX-FiXy-L-IeGZRvUR4W4g6zufe-R9kOghXQ7x0IEAA; SIDCC=APoG2W8kybJvEUEm3YT63zrhKiQf3I3RVWh8svdLupKdUxPZTkitquUZA33e2ddQk_yoA7eNsQ; __Secure-1PSIDCC=APoG2W-bcAtrzl7Inf0LJ9GWvMwGweUl_PXQAfGyjpwbVuzV8JDNZOtPOPZ2wxGtnsupYRO6OQ; __Secure-3PSIDCC=APoG2W_99wD2POZn5DgYGZg9eyCXMMq0KrGXT7Yu6wSL3zjfePnstZUJ-SrReKUFS5Sp0Lpnl6g',
        'origin': 'https://drive.google.com',
        'referer': 'https://drive.google.com/u/0/uc?id=1Z9ox9W8dyDujc_V68o3HFnQ26LtFxyzP&export=download',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"115.0.5790.171"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.171", "Chromium";v="115.0.5790.171"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-chrome-connected': 'source=Chrome,id=118370280517983187392,mode=0,enable_account_consistency=false,consistency_enabled_by_default=false',
        'x-client-data': 'CI+2yQEIpLbJAQipncoBCI7lygEIlaHLAQiEk80BCIWgzQEI3L3NAQi7vs0BCODEzQEI7sTNAQigxc0BCOjFzQEItsjNAQjxyc0BCLnKzQEI7crNAQjQy80BGImnzQE=',
    }
    try:
        response = requests.post(
            f'https://drive.google.com/u/0/uc?id={full.group(1)}&export=download&confirm=t&uuid=beb5a318-029a-4e58-b861-e32f1539b440&at=AB6BwCAuKvsnc2OqX4QPaGiAs1R1:1692222547387',
            headers=headers,allow_redirects=True
        )
        if response.status_code == 404:
            return 404
        else:
            open(filename, 'wb').write(response.content)
            return True
    except Exception as error:
        print(error)
        return False

def upbaam(url:str,filename:str) -> bool:
    full = re.match('http://upbaam\.com/(.*?)$',url)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en,ar;q=0.9,en-US;q=0.8,uz;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'lang=english; aff=2919',
        'Origin': 'http://upbaam.com',
        'Referer': 'http://upbaam.com/m0r1q58unnxa',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    data = {
        'op': 'download2',
        'id': full.group(1),
        'rand': '',
        'referer': url,
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        bitit = bs4.BeautifulSoup(response.content, 'html.parser')
        rt = bitit.find('span', attrs={'id': 'direct_link'}).find('a').get('href')
        doit = requests.get(rt)
        open(filename,'wb').write(doit.content)
        return True
    except:
        return False

def get_upload_info(url:str) -> dict:
    re1 = requests.get(url)
    bs = bs4.BeautifulSoup(re1.content,'html.parser')
    oar = bs.find('script',attrs={'type':'application/ld+json'})
    dumping = str(oar).replace('<script type="application/ld+json">','').replace('</script>','')
    return json.loads(dumping)

def sub(id,token,ch):
    try:
        response = requests.get(
            f'https://api.telegram.org/bot{token}/getChatMember?chat_id=@{ch}&user_id={}'.format(
                id)).json()
        if response["ok"]:
            if "left" in str(response):
                return False
            else:
                return True
        elif response["ok"] == False:
            return False
    except Exception as e:  #
        print(e)
        return True

def get_from_the_main_page(typ:str):
    r1 = requests.get('https://animelek.me/')
    bit = bs4.BeautifulSoup(r1.content,'html.parser')
    results = {}
    if typ == 'MostEspView':
        bit2 = bit.find('div',attrs={'class':'slider-episode-container'}).find_all('div',attrs={'id':'main','class':'hover'})
        for res in bit2:
            results[res.find_next('img').get('alt').replace('AnimeLek','').replace('انمي ليك',"").replace(' ','')] = res.find_next('a').get('href')
    elif typ == "PinnedEsp":
        bit2 = bit.find_all('div', attrs={'class': 'episodes-card-container'})
        for res in bit2:
            results[res.find_next('img').get('alt').replace('AnimeLek', '').replace('انمي ليك', "").replace(' ',
                                                                                                            '')] = res.find_next(
                'a').get('href')
    elif typ == "PinnedAnimes":
        bit2 = bit.find('div', attrs={'class': 'anime-list-content'}).find_all('div',attrs={'class':'anime-card-container'})
        for pipr in bit2:
            results[pipr.find_next('h3').text] = pipr.find_next('a').get('href')
    return results

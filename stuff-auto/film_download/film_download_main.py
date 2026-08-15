import httpx
import time
import random

# ------------------------------------------------------------
# input movie or series : [1] or [2]
# input movie/series name

# search movie in db : [name, release_date, movie_id, specified_string, image_url,]

# movies/series { the difference is the uri only }
# movies uri => [ movie_id, specified_string ]
# series uri => [ movie_id, specified_string, season, episode ]

# switch the download link params with info and extract : [480p] data

# Download [ Retrieve the uri after the hostname and use as new uri for download request ]

# Naming convention Series => Show_season_episode { user's initial input }
# Naming convention Movies => movie_name { user's initial input }
# ------------------------------------------------------------

link_headers = {
    'Host': 'h5-api.aoneroom.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'x-request-lang': 'en',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjMwNTUzODY3NjE4NTk0MTgzMjgsImF0cCI6MywiZXh0IjoiMTc4NjI4MDY1NSIsImV4cCI6MTc5NDA1NjY1NSwiaWF0IjoxNzg2MjgwMzU1fQ.ewouykSDDP-lP3LN16ER4GQkSQwoMEqyWzv3g2cSHTE',
    'X-Client-Info': '{"timezone":"Pacific/Honolulu"}',
    'Origin': 'https://videodownloader.site',
    'Connection': 'keep-alive',
    'Referer': 'https://videodownloader.site/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site'
    }
video_headers = {
    'Host': 'bcdnxw.hakunaymatata.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive',
    'Referer': 'https://videodownloader.site/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i'
    }


def main_function():

    search_name = input("Name of the Series/Movie :")
    result_amount = int(input("Max return of search results :"))

    # ----------------------[search]--------------------
    url = "https://h5-api.aoneroom.com/wefeed-h5api-bff/subject/search" 

    payload = {
        "keyword":search_name,
        "page":1,
        "perPage":result_amount,
        "subjectType":0
        }

    custom_headers = {
        'Host': 'h5-api.aoneroom.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'x-request-lang': 'en',
        'X-Source': 'downloader',
        'X-Client-Info': '{"timezone":"Pacific/Honolulu"}',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjMwNTUzODY3NjE4NTk0MTgzMjgsImF0cCI6MywiZXh0IjoiMTc4NjI4MDY1NSIsImV4cCI6MTc5NDA1NjY1NSwiaWF0IjoxNzg2MjgwMzU1fQ.ewouykSDDP-lP3LN16ER4GQkSQwoMEqyWzv3g2cSHTE',
        'Origin': 'https://videodownloader.site',
        'Connection': 'keep-alive',
        'Referer': 'https://videodownloader.site/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
        }
    
    response = httpx.post(url, json=payload, headers=custom_headers)
    print(response.status_code)
    # -------------------------------------------------

    search_results = response.json()['data']['items']
    curated_search_results = []

    for item in search_results:
        item_number = len(curated_search_results)

        restructured_data = {
                "item_no": int(item_number + 1),
                "item_id": item['subjectId'],
                "item_string": item['detailPath'],
                "release_date": item['releaseDate'],
                "title": item['title'],
                "thumbnail": item['cover']['url']
                }

        curated_search_results.append(restructured_data)    
        
    for found_result in curated_search_results:
        print('----------------------------------------')
        print(found_result)

    chosen_result_input = int(input("Show number chosen to proceed :"))
    show_category = input("Put [1] for Movie or [2] for Series :")

#movie
    if show_category == "1":

    # ------------------[links]---------------
        url = 'https://h5-api.aoneroom.com/wefeed-h5api-bff/subject/download'

        query_params = {
            'subjectId':curated_search_results[chosen_result_input]['item_id'],
            'detailPath':curated_search_results[chosen_result_input]['item_string']
            }

        
        response = httpx.get(url, params=query_params, headers=link_headers)
        res_download_link_dicts = response.json()['data']['downloads']
        print(res_download_link_dicts)
    # -------------------------------------------------

        get_download_link = []

        for res_obj in res_download_link_dicts:
            if res_obj['resolution'] == 480:
                get_download_link.append(res_obj['url'])
                continue
            elif res_obj['resolution'] == 720:
                get_download_link.append(res_obj['url'])
                continue
        # --------------------[download_file]-----------------
        try:
            video_url = get_download_link[0]
            print(f'video url :{video_url}')

                
                # Stream the download to handle large files safely
            with httpx.stream("GET", video_url, headers=video_headers, follow_redirects=True) as response:
                response.raise_for_status()
                with open(f"{search_name}.mp4", "wb") as f:
                    for chunk in response.iter_bytes(chunk_size=1000192):
                        f.write(chunk)
                
            print(f"{search_name} download complete!")

        except:
            print(f"{search_name} had issues thus skipped")
        # -------------------------------------------------


#series
    if show_category == "2":

        season_number_input = int(input("Season Number:"))
        episode_number_list_input = input("Episode to download separated by comma symbol:")

        episode_number_list = episode_number_list_input.split(",") 
        amount_of_episodes = len(episode_number_list)
        current_iteration = 0

        while current_iteration < amount_of_episodes:
            
            current_episode = int(episode_number_list[current_iteration])
            episode_name = f"{search_name}_sn{season_number_input}_ep{current_episode}"

        # --------------------[links]-----------------
            url = 'https://h5-api.aoneroom.com/wefeed-h5api-bff/subject/download'

            query_params = {
                'subjectId':curated_search_results[chosen_result_input]['item_id'],
                'se':season_number_input,
                'ep':current_episode,
                'detailPath':curated_search_results[chosen_result_input]['item_string']
                }

            
            response = httpx.get(url, params=query_params, headers=link_headers)
            res_download_link_dicts = response.json()['data']['downloads']
            print(res_download_link_dicts)
            # -------------------------------------------------

            get_download_link = []

            for res_obj in res_download_link_dicts:
                if res_obj['resolution'] == 480:
                    get_download_link.append(res_obj['url'])
                    continue
                elif res_obj['resolution'] == 720:
                    get_download_link.append(res_obj['url'])
                    continue
        # --------------------[download_file]-----------------
            try:
                video_url = get_download_link[0]
                print(f'video url :{video_url}')

                
                # Stream the download to handle large files safely
                with httpx.stream("GET", video_url, headers=video_headers, follow_redirects=True) as response:
                    response.raise_for_status()
                    with open(f"{episode_name}.mp4", "wb") as f:
                        for chunk in response.iter_bytes(chunk_size=1000192):
                            f.write(chunk)
                
                print(f"{episode_name} download complete!")

            except:
                print(f"{episode_name} had issues thus skipped")
        # -------------------------------------------------

            time.sleep(random.randint(7,13))
            current_iteration += 1


main_function()



import requests, sys, time, os, argparse

import json

# List of simple to collect features
snippet_features = ["title", "publishedAt", "channelTitle"]


def setup(api_path, code_path):
    with open(api_path, "r") as file:
        api_key = file.readline()

    with open(code_path) as file:
        country_codes = [x.rstrip() for x in file]

    return api_key, country_codes


def api_request(page_token, country_code):
    # Builds the URL and requests the JSON from it
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=5&key={api_key}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    return request.json()


def get_videos(items):
    lines = []
    for video in items:
        # We can assume something is wrong with the video if it has no statistics, often this means it has been deleted
        # so we can just skip it
        if "statistics" not in video:
            continue

        # A full explanation of all of these features can be found on the GitHub page for this project
        video_id = video["id"]

        # Snippet and statistics are sub-dicts of video, containing the most useful info
        snippet = video["snippet"]

        # This list contains all of the features in snippet that are 1 deep and require no special processing
        features = [(snippet.get(feature, "")) for feature in snippet_features]

        # The following are special case features which require unique processing, or are not within the snippet dict
        thumbnail_link = (
            snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        )
        trending_date = time.strftime("%y.%d.%m")

        # Compiles all of the various bits of info into one consistently formatted line
        line = {
            "id": video_id,
            "features": features,
            "trending_date": (trending_date),
            "thumbnail_link": (thumbnail_link),
        }
        lines.append(line)
    return lines


def get_pages(country_code, next_page_token="&"):
    country_data = []

    # Because the API uses page tokens (which are literally just the same function of numbers everywhere) it is much
    # more inconvenient to iterate over pages, but that is what is done here.
    while next_page_token is not None:
        # A page of data i.e. a list of videos and all needed data
        video_data_page = api_request(next_page_token, country_code)

        # Get the next page token and build a string which can be injected into the request with it, unless it's None,
        # then let the whole thing be None so that the loop ends after this cycle
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = (
            f"&pageToken={next_page_token}&"
            if next_page_token is not None
            else next_page_token
        )

        # Get all of the items as a list and let get_videos return the needed features
        items = video_data_page.get("items", [])
        country_data += get_videos(items)

    return country_data


def write_to_file(country_code, country_data):

    print(f"Writing {country_code} data to file...")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f"{output_dir}/{country_code}_videos_data.json", "w+") as file:
        file.write(json.dumps(country_data))


def get_data():
    for country_code in country_codes:
        country_data = get_pages(country_code)
        write_to_file(country_code, country_data)


if __name__ == "__main__":

    key_path = "api_key.txt"
    country_code_path = "country_codes.txt"
    output_dir = "output/"

    api_key, country_codes = setup(key_path, country_code_path)

    get_data()

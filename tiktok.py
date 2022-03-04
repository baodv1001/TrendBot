from TikTokApi import TikTokApi

api = TikTokApi(custom_verify_fp="verify_l0536qsy_sOkSW67e_nCSj_4Lry_AJoF_1F223Bk2A5IR")
#api = TikTokApi()

for trending_video in api.trending.videos():
    # Prints the author's username of the trending video.
    print(trending_video.author.username)

from TikTokApi import TikTokApi

api = TikTokApi(custom_verify_fp="verify_kzr77pdk_r71ff1Se_d5cB_4egT_AXQC_4sGyPfY3ZYHc")
#api = TikTokApi()

for trending_video in api.trending.videos(count=10):
    # Prints the author's username of the trending video.
    print(trending_video)

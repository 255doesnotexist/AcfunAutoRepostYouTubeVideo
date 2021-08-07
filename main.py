from config import *
import pyyoutube
import os
import json


def get_videos(channel_name = "UCnGsBkjtNacIi9qX3WbU20Q"): # 获取该频道下所有视频
    api = pyyoutube.Api(api_key=API_KEY)
    channel_res = api.get_channel_info(channel_name=channel_name)

    playlist_id = channel_res.items[0].contentDetails.relatedPlaylists.uploads

    playlist_item_res = api.get_playlist_items(
        playlist_id=playlist_id, count=10, limit=6
    )

    videos = []
    for item in playlist_item_res.items:
        video_id = item.contentDetails.videoId
        video_res = api.get_video_by_id(video_id=video_id)
        videos.extend(video_res.items)
    return videos

def update_processed_json(processed = dict()): # 把处理过的视频记录进processed.json中 效率不高
    with open('processed.json','w') as f:
        f.write(json.dumps(processed))


def processor(channel_name = "UCnGsBkjtNacIi9qX3WbU20Q", processed = dict()): # 处理每个监视的频道
    videos = get_videos(channel_name)

    for video_obj in videos:
        video = json.loads(video_obj.to_json())
        if str(video['id']) in processed:
            continue
        print('YouTube视频ID：'+video['id']+'\n') # for debug
        print('视频标题：'+video['snippet']['title']+'\n')
        print('视频详情：'+video['snippet']['description']+'\n')
        print('视频播放量：'+video['statistics']['viewCount']+'\n')
        print('视频点赞量：'+video['statistics']['likeCount']+'\n')
        print('视频点踩量：'+video['statistics']['dislikeCount']+'\n')
        print('视频评论量：'+video['statistics']['commentCount']+'\n')
        print('视频封面URL：'+video['snippet']['thumbnails']['default']['url']+'\n')
        print('视频语言：'+video['snippet']['defaultAudioLanguage']+'\n')
        print('视频发布时间：'+video['snippet']['publishedAt']+'\n')
        print('视频URL：https://www.youtube.com//watch?v='+video['id']+'\n')
        print("\n")
        processed[video['id']] = True
        update_processed_json(processed)

def get_processed_video_dict(): # 处理过的视频列表获取
    str=''
    if(os.path.isfile('processed.json')):
        with open('processed.json', 'r') as f:
            str=str+f.read()
    else:
        str='{}'
    if str == '':
        str = '{}'
    return json.loads(str)

if __name__ == "__main__":
    processed = get_processed_video_dict()
    for channels in CHANNELS_WATCHING_ON:
        processor(channels, processed = processed)

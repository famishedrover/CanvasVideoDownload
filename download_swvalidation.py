"""
Download videos from S W and Testing Course @ASU Canvas.

Problem : 
The default canvas setting for the videos is 360p or 540p. If we select 1080, then we get the correct m3u8 file, however that's a manual process. Moreover, clicking the 1080
thing, generates a new m3u8 filename which would have to be further parsed. 

To check if m3u8 have tags for 1080?



Solution TODO.

It seems that the iframe tag in the HTML contains a <script> that has all the links as <link>.bin (search for 1080p).
But we still need an automated solution to browse through all the webpages and collect tehse links.

"""


# # 
# def download(m3u8_uri, max_retry_times=3, max_num_workers=100,
#              mp4_file_dir='./', mp4_file_name='m3u8_To_Mp4.mp4', tmpdir=None):

import json
import m3u8_To_MP4 as mpp
import os

import threading



# read links from JSON dump log of firefox. 

def read_json(json_path)  :
	with open(json_path, 'r') as f :
		data = json.load(f)
	return data 

def get_links_from_json(json_path, no_ts=True) :
	"""
	json_path: path of the json file to parse.
	no_ts: TS are segment pieces of m3u8 playlist. Usually we don't need those, so mark this as True.
	""" 
	data = read_json(json_path)

	media_entries = data['log']['entries']

	media_urls = [ix['request']['url'] for ix in media_entries]

	no_ts_media_urls = []
	for ix in media_urls : 
		if ".ts" not in ix : 
			no_ts_media_urls.append(ix)

	return no_ts_media_urls


def download_playlist(links, save_path) : 

	for ix, link in enumerate(links) : 
		mpp.download(link, mp4_file_dir=save_path, mp4_file_name=str(ix)+".mp4")



def process_single_unit(unit) :
		SAVE_DIR = "./videos/"

		UNIT_NAME = 'unit-' + str(unit) + ".har"
		UNIT_PATH = "./data/" + UNIT_NAME

		SAVE_PATH = SAVE_DIR + UNIT_NAME
		if not os.path.exists(SAVE_PATH):
			os.makedirs(SAVE_PATH)
		playlist_links = get_links_from_json(UNIT_PATH)
		download_playlist(playlist_links, save_path = SAVE_PATH)


def run_this(units):
	THREADS = []

	for ix in (range(len(units))) :
		NAME = 'thread' + str(ix)
		tmp = threading.Thread(target=process_single_unit, name=NAME, args=(units[ix],))
		THREADS.append(tmp)
		tmp.start()

	for ix in len(THREADS) : 
		THREADS[ix].join()

	print ("[INFO] Finished")





if __name__ == "__main__" : 
	UNIT_NAMES = list(range(1,5))
	run_this(UNIT_NAMES)









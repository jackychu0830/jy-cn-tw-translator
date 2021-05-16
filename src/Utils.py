import platform
import os


def get_jy_path():
    if platform.system().lower() == 'windows':
        return os.path.expanduser('~') + '\\AppData\\Local\\JianyingPro\\User Data\\Projects\\com.lveditor.draft'
    else:
        return os.path.expanduser('~') + '/Movies/JianyingPro/User Data/Projects/com.lveditor.draft'


def get_video_info_filename(path):
    if platform.system().lower() == 'windows':
        return path + '\\draft_info.json'
    else:
        return path + '/draft_info.json'


def get_video_meta_filename(path):
    if platform.system().lower() == 'windows':
        return path + '\\draft_meta_info.json'
    else:
        return path + '/draft_meta_info.json'


def get_cover_image_filename(path):
    if platform.system().lower() == 'windows':
        return path + '\\draft_cover.jpg'
    else:
        return path + '/draft_cover.jpg'


def get_export_srt_filename(filename):
    if platform.system().lower() == 'windows':
        return os.path.expanduser('~') + '\\Desktop\\' + filename + '.srt'
    else:
        return os.path.expanduser('~') + '/Desktop/' + filename + '.srt'

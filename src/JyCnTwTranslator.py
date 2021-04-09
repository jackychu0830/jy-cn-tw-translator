import json
import os

from pygoogletranslation import Translator

JY_PATH = os.path.expanduser('~') + '/Movies/JianyingPro/videocut/'


def get_video_texts(filename):
    """
    Get all text content from video
    :param filename: file name
    :return: all subtitle in list format
    """
    f = open(filename)
    txt = f.read()
    f.close()

    json_obj = json.loads(txt)
    texts = []
    for text in json_obj.get('materials').get('texts'):
        texts.append(text.get('content'))

    return texts


def set_video_texts(new_texts, filename):
    """
    Write translated texts back to video

    :param new_texts: Translated texts
    :param filename: file name
    """
    f = open(filename)
    txt = f.read()
    f.close()
    json_obj = json.loads(txt)
    for i in range(0, len(new_texts)):
        # print(json_obj['materials']['texts'][i]['content'] + ' -> ' + new_texts[i])
        json_obj['materials']['texts'][i]['content'] = new_texts[i]

    with open(filename, 'w', encoding='utf8') as json_file:
        json.dump(json_obj, json_file, ensure_ascii=False)


def do_translate(cn_texts):
    """
    Do translate from CN to TW
    
    :param cn_texts: Texts in CN
    :return: Texts in TW
    """
    translator = Translator()
    result = translator.translate(cn_texts, src='zh-cn', dest='zh-tw')
    tw_texts = [r.text for r in result]

    return tw_texts


def main():
    jy_video = input('Please input video id: ')
    filename = JY_PATH + jy_video + '/template.json'
    cn_texts = get_video_texts(filename)
    print(cn_texts)

    tw_texts = do_translate(cn_texts)
    print(tw_texts)
    set_video_texts(tw_texts, filename)


if __name__=="__main__":
    main()


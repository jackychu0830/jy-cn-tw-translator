import json
import os

from pygoogletranslation import Translator

JY_PATH = os.path.expanduser('~') + '/Movies/JianyingPro/videocut/'


def get_subtitle_text(filename):
    """
    Get all subtitle text from file
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


def set_subtitle_text(new_texts, filename):
    """
    Write translated subtitle back to JT file

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


def main():

    jy_video = input('Please input video id: ')
    filename = JY_PATH + jy_video + '/template.json'
    cn_text = get_subtitle_text(filename)
    print(cn_text)

    translator = Translator()
    result = translator.translate(cn_text, src='zh-cn', dest='zh-tw')
    tw_text = [r.text for r in result]
    print(tw_text)

    set_subtitle_text(tw_text, filename)


if __name__=="__main__":
    main()


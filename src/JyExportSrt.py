# Copyright: https://github.com/yinbaiyuan/JYToSRT

import json


def analyseFile(jsonStr=''):
    json_obj = json.loads(jsonStr)
    texts = json_obj['materials']['texts']
    tracks = json_obj['tracks']
    subtitleDic = {}
    for textInfo in texts:
        tKey = textInfo['id']
        tValue = {'content': textInfo['content']}
        subtitleDic[tKey] = tValue
    for trackInfo in tracks:
        segments = trackInfo['segments']
        for segment in segments:
            mId = segment['material_id']
            if mId in subtitleDic.keys():
                subtitleInfo = subtitleDic[mId]
                subtitleInfo['start'] = segment['target_timerange']['start']
                subtitleInfo['duration'] = segment['target_timerange']['duration']
                subtitleDic[mId] = subtitleInfo
    subtitleDic = sorted(subtitleDic.items(), key=lambda x: x[1]['start'], reverse=False)
    return subtitleDic


def msToTimeStr(t=0):
    res = ''
    ms = t // 1000 % 1000
    sec = t // 1000 // 1000 % 60
    min = t // 1000 // 1000 // 60 % 60
    hour = t // 1000 // 1000 // 60 // 60
    res += "%02d" % hour + ':' + "%02d" % min + ':' + "%02d" % sec + ',' + "%03d" % ms
    return res


def createSrt(subtitleDic):
    srtStr = ''
    subtitleCount = 1
    for subtitle in subtitleDic:
        srtStr += str(subtitleCount)
        srtStr += '\n'
        subtitleCount += 1
        startTimeStr = msToTimeStr(subtitle[1]['start'])
        endTimeStr = msToTimeStr(subtitle[1]['start'] + subtitle[1]['duration'])
        srtStr += startTimeStr + ' --> ' + endTimeStr
        srtStr += '\n'
        srtStr += subtitle[1]['content']
        srtStr += '\n'
        srtStr += '\n'
    return srtStr

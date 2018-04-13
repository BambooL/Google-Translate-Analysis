# -*- coding: utf-8 -*-
"""
You need to fill in your API key from google below. Note that querying
supported languages is not implemented.
"""
import os
import urlparse
import urllib
import urllib2
import httplib2
import gzip
import json
from httplib2 import FileCache
from urllib2 import HTTPRedirectHandler, HTTPDefaultErrorHandler, HTTPError

### Hard-coded variables ###

api = 'AIzaSyCHlx9P2HTmmgJRmDfUtZZTqZtPhtIU0bA'

languages = ["af", "sq", "ar","be", "bg", "ca", "zh-CN", "zh-TW", "hr",
             "cs", "da", "nl", "en", "et", "tl", "fi", "fr", "gl", "de",
             "el", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "ko",
             "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro",
             "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk",
             "vi", "cy", "yi"]

def _validate_language(lang):
    if lang in languages:
        return True
    return False

### Custom G-Zipped Cache ###

def save_cached_key(path, value):
    f = gzip.open(path, 'wb')
    f.write(value)
    f.close()

def load_cached_key(key):
    f = gzip.open(key)
    retval = f.read()
    f.close()
    return retval

class ZipCache(FileCache):
    def __init__(self, cache='.cache'): #TODO: allow user configurable?
        super(ZipCache, self).__init__(cache)

    def get(self, key):
        cacheFullPath = os.path.join(self.cache, self.safe(key))
        retval = None
        try:
            retval = load_cached_key(cacheFullPath)
        except IOError:
            pass
        return retval

    def set(self, key, value):
        retval = None
        cacheFullPath = os.path.join(self.cache, self.safe(key))
        save_cached_key(cacheFullPath, value)

### Error Handlers ###

class DefaultErrorHandler(HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = HTTPError(req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result


class RedirectHandler(HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = HTTPRedirectHandler.http_error_301(self, req, fp, code,
                        msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        results = HTTPRedirectHandler.http_error_302(self, req, fp, code,
                        msg, headers)
        results.status = code
        return result

### Translator Class ###

class GoogleTranslator(object):
    """
    Google Translator object.

    Examples
    --------
    translator = GoogleTranslator()

    results1 = translator.translate("Einen schönen Tag allerseits")

    # try 2 at a time
    results2 = translator.translate(["Einen schönen Tag allerseits",
                                     "Ich nehme an"])

    # try detect
    results3 = translator.detect("Einen schönen Tag allerseits")

    # try to detect 2 at a time
    results4 = translator.detect(["Einen schönen Tag allerseits",
                                     "Ich nehme an"])
    """
    def __init__(self):
        #NOTE: caching is done on etag not expiry
        self.cache_control = 'max-age='+str(7 * 24 * 60 * 60)
        self.connection = httplib2.Http(ZipCache())
        self._opener = urllib2.build_opener(DefaultErrorHandler,
                                            RedirectHandler)
        self.base_url = "https://www.googleapis.com/language/translate/v2/"

    def _urlencode(self, params):
        """
        Rewrite urllib.urlencode to handle string input verbatim
        """
        params = "&".join(map("=".join,params))
        return params

    def _build_uri(self, extra_url, params):
        params = [('key', api)] + params
        params = self._urlencode(params)
        url = "%s?%s" % (urlparse.urljoin(self.base_url, extra_url), params)
        if len(url) > 2000: # for GET requests only, POST is 5K
            raise ValueError("Query is too long. URL can only be 2000 "
                             "characters")
        return url

    def _fetch_data(self, url):
        connection = self.connection
        resp, content = connection.request(url, headers={'user-agent' : api,
                            'cache-control' : self.cache_control})
        #DEBUG
        #if resp.fromcache:
        #   print "Using from the cache"
        return content

    def _sanitize_query(self, query):
        if isinstance(query, (list,tuple)):
            query = zip('q' * len(query), map(urllib.quote,query))
        else:
            query = [('q',urllib.quote(query))]
        return query

    def _decode_json(self, response):
        """
        Assumes that response only holds one result
        """
        json_data = json.loads(response)
        try:
            data = json_data["data"]
            if 'translations' in data:
                return data['translations']
            elif 'detections' in data:
                return data['detections']
        except:
            if 'error' in json_data:
                return json_data["error"]


    def detect(self, query):
        """
        Try to detect the language of a word, phrase, or list of either.

        Parameters
        ----------
        query : str or iterable
            Query or list of queries to translate

        Returns
        -------
        List of dictionaries for each query
        """
        query = self._sanitize_query(query)
        url = self._build_uri(extra_url='detect/', params=query)
        content = self._fetch_data(url)
        # going to have json, decode it first
        return self._decode_json(content)

    def translate(self, query, target="en", source="", _dirty=False):
        """
        Translate a query.

        Parameters
        ----------
        query : str or iterable
            Query or list of queries to translate
        target : str
            Language to translate into.
        source : str, optional
            Language of the source text, if known. Will be auto-detected
            if an empty string is passed.
        dirty : bool
            This is not intended to be used by users. It is here to avoid
            infinite recursion if the query returns an error because the
            language can't be detected.

        Returns
        -------
        List of dictionaries for each query

        Notes
        -----
        If the language can't be detected for a word an attempt is made
        to detect the language of the word and resubmit the query. If a
        list of words to translate is given and an error is encountered,
        it is assumed that the list of words all have the same source language
        when resubmitted.
        """
        try:
            assert _validate_language(target)
        except:
            raise ValueError("target language %s is not valid" % target)
        newquery = self._sanitize_query(query)
        params = [('key', api), ('target' , target)]
        if source:
            try:
                assert _validate_language(target)
            except:
                raise ValueError("source language %s is not valid" % target)
            params += ["source", source]
        params += newquery
        url = self._build_uri("", params)
        content = self._fetch_data(url)
        results = self._decode_json(content)

        if "errors" in results and not _dirty:
            if results['message'] == 'Bad language pair: {0}':
                # try to detect language and resubmit query
                source = self.detect(query)
                source = source[0]['language']
                return self.translate(query, target, source, True)

        return results

if __name__ == "__main__":
    result = {}
    translator = GoogleTranslator()
    # university_list = ["北京大学", "中国人民大学", "清华大学", "北京交通大学", "北京工业大学", "北京航空航天大学", "北京理工大学", "北京科技大学", "北京化工大学", "北京邮电大学", "中国农业大学", "北京林业大学", "北京中医药大学", "北京师范大学", "北京外国语大学", "中国传媒大学", "中央财经大学", "对外经济贸易大学", "北京体育大学", "中央音乐学院", "中央民族大学", "中国政法大学", "华北电力大学", "南开大学", "天津大学", "天津医科大学", "河北工业大学", "太原理工大学", "内蒙古大学", "辽宁大学", "大连理工大学", "东北大学", "大连海事大学", "吉林大学", "延边大学", "东北师范大学", "哈尔滨工业大学", "哈尔滨工程大学", "东北农业大学", "东北林业大学", "复旦大学", "同济大学", "上海交通大学", "华东理工大学", "东华大学", "华东师范大学", "上海外国语大学", "上海财经大学", "上海大学", "第二军医大学", "南京大学", "苏州大学", "东南大学", "南京航空航天大学", "南京理工大学", "中国矿业大学", "河海大学", "江南大学", "南京农业大学", "中国药科大学", "南京师范大学", "浙江大学", "安徽大学", "中国科学技术大学", "合肥工业大学", "厦门大学", "福州大学", "南昌大学", "山东大学", "中国海洋大学", "中国石油大学", "郑州大学", "武汉大学", "华中科技大学", "中国地质大学", "武汉理工大学", "华中农业大学", "华中师范大学", "中南财经政法大学", "湖南大学", "中南大学", "湖南师范大学", "国防科学技术大学", "中山大学", "暨南大学", "华南理工大学", "华南师范大学", "广西大学", "海南大学", "四川大学", "西南交通大学", "电子科技大学", "四川农业大学", "西南财经大学", "重庆大学", "西南大学", "贵州大学", "云南大学", "西藏大学", "西北大学", "西安交通大学", "西北工业大学", "西安电子科技大学", "长安大学", "西北农林科技大学", "陕西师范大学", "第四军医大学", "兰州大学", "青海大学", "宁夏大学", "新疆大学", "石河子大学"]
    university_list = ["北京大学"]
    counter = 0
    for i in range(1000):
        try:
            sentence = "北大不如清华"
            trans = translator.translate(sentence)
            print trans[0]['translatedText']
        except:
            print "Error!"
    # for u1 in university_list:
    #     for u2 in university_list:
    #         try:
    #             sentence = u1 + "不如" + u2
    #             trans = translator.translate(sentence)
    #             print sentence
    #             print trans[0]['translatedText']
    #         except:
    #             print "Error!"

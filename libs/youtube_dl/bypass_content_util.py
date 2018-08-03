import io
import json
import traceback
from httplib import HTTPMessage
from urllib import addinfourl
from YoutubeDLApi.settings import youtubedl_logger

class BypassContent(object):

    def response(self, url, bypass_content): # bypass_content: { url1: [content, headers],
        try:
            data = json.loads(bypass_content)
            if url in data:
                d = data[url]
                fp = io.BytesIO(d[0].encode('utf-8'))
                headers = HTTPMessage(io.StringIO(unicode(d[1])), 0)
                # for head in d[1].split("\n"):
                #     xy = head.split(":")
                #     headers.addheader(xy[0].strip(), xy[1].strip())

                url = url
                code = 200
                msg = 'OK'
                res = addinfourl(fp, headers, url, code)
                youtubedl_logger.info('Request Bypassed for url -> '+ url)
                return res
            else:
                youtubedl_logger.info('Request Skipped for url -> ' + url)
                return None
        except Exception as e:
            youtubedl_logger.info('Request Exception for url -> ' + url)
            traceback.print_exc()
            return None

import io
import json
import traceback
from httplib import HTTPMessage
from urllib import addinfourl

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
                return res
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            return None

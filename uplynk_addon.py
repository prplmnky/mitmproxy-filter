from mitmproxy import ctx
from xhostmatcher import XHostMatcher
import re

# Alter Uplynk m3u8 playlist to remove ad segments
class Uplynk:
    def __init__(self):
        self.server_mitm_hosts = XHostMatcher(['uplynk'])

    def response(self, flow):
        if(flow.server_conn.address is None):
            return

        server = flow.server_conn.address[0]
        if(not self.server_mitm_hosts(server)):
            return

        ct = flow.response.headers["content-type"].lower()
        if(ct is not None and ct.find("mpegurl") != -1):
            ctx.log.info("PASS: found video playlist")
            newcontent=""
            if(flow.response.content is not None):
                content = flow.response.content
            elif(flow.response.text is not None):
                content = flow.response.text
            else:
                content = flow.response.raw_content

            if(content is None):
                ctx.log.info("PASS: empty playlist response")
                return
        

            found=False
            #discontinuity=0
            ctx.log.info("PASS: response\n %s" % content)
            for line in content.splitlines():
                #print("PASS: %s" % line)
                if(re.compile("UPLYNK-SEGMENT:.*?,ad").search(line.decode("utf-8"))):
                    found=True
                    ctx.log.info("PASS: removing ad")
                    continue
                if(re.compile("UPLYNK-SEGMENT:.*?,segment").search(line.decode("utf-8"))):
                    found=False
                #if(re.compile("EXT-X-DISCONTINUITY").search(line.decode("utf-8"))):
                #    discontinuity=1
                #if(discontinuity > 0 and discontinuity < 3):
                #    discontinuity += 1
                #    continue
                #else:
                #    discontinuity = 0
                if(not found):
                    ctx.log.info("PASS: %s" % line)
                    newcontent+=line.decode("utf-8") + '\n'

            if(newcontent):
                flow.response.content=newcontent.encode("utf-8")

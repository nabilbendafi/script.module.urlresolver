"""
    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import base64
import urllib
from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin

class TrollVidResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "trollvid.net"
    domains = ["trollvid.net"]
    
    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()
        self.pattern = '//((?:sv\d*\.)?trollvid\.net)/embed\.php.file=([0-9a-zA-Z]+)'
    
    def get_url(self, host, media_id):
            return 'http://trollvid.net/embed.php?file=%s' % media_id

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r: return r.groups()
        else: return False
    
    def valid_url(self, url, host):
        return re.search(self.pattern, url) or self.name in host
    
    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)

        html = self.net.http_GET(web_url).content

        try: stream_url = re.search('url\s*:\s*"(http.+?)"', html).group(1)
        except: pass

        try: stream_url = re.search('atob\(\'(.+?)\'', html).group(1)
        except: pass

        try: stream_url = base64.b64decode(stream_url)
        except: pass

        try: stream_url = urllib.unquote_plus(stream_url)
        except: pass

        return stream_url

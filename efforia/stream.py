import gdata.youtube
import gdata.media
import json
from xml.dom.minidom import parseString
from main import Efforia

apis = json.load(open('efforia/settings.json','r'))
google_api = apis['social']['google']

class StreamService(Efforia):
    def __init__(self):
        self.developer_key = "AI39si7wyQ0h6KhpWLhZfJa-U4mU65rO3Dj-05grmYkZk-kn_sv8br5UdDIEORwG-itcRn5wSBTFbgu02KyR_FhSQNaR0QbvSQ"
        self.client_id = google_api['client_id']
    def videos_by_user(self,username):
        uri = 'https://gdata.youtube.com/feeds/api/users/%s/uploads?alt=json' % username
        return self.do_request(uri)
    def video_thumbnail(self,token,access_token):
        actoken = self.refresh_google_token(access_token)
        uri = 'https://gdata.youtube.com/feeds/api/users/default/uploads/%s?access_token=%s' % (token,actoken)
        thumbnail = parseString(self.do_request(uri)).getElementsByTagName('media:thumbnail')[0].attributes['url'].value
        return str(thumbnail)
    def video_entry(self,title,description,keywords,access_token):
        media_group = gdata.media.Group(title=gdata.media.Title(text=title),
                                        description=gdata.media.Description(description_type='plain',text=description),
                                        keywords=gdata.media.Keywords(text='efforia'),
                                        category=[gdata.media.Category(text='Entertainment',
                                                                       scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                                                                       label='Entertainment')],
                                        player=None)
                                        #private=gdata.media.Private())
        video_entry = gdata.youtube.YouTubeVideoEntry(media=media_group)
        url,token = self.get_upload_token(video_entry,access_token)
        return url,token

    def get_upload_token(self,video_entry,access_token):
        actoken = self.refresh_google_token(access_token)
        print actoken
        headers = {
                   'Authorization': 'OAuth %s' % actoken,
                   'X-gdata-key': 'key=%s' % self.developer_key,
                   'Content-type': 'application/atom+xml'
        }
        response = self.do_request('https://gdata.youtube.com/action/GetUploadToken',str(video_entry),headers)
        print response
        url = parseString(response).getElementsByTagName('url')[0].childNodes[0].data
        token = parseString(response).getElementsByTagName('token')[0].childNodes[0].data
        return url,token

    def search_video(self,search_terms):
        pass

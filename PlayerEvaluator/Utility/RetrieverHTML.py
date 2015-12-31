import urllib.request
import urllib.response
import urllib.parse
import http.cookiejar
from PlayerEvaluator.Utility.HTML_Consts import Consts


class RetrieverHTML:
    email = None
    password = None
    cookie = None
    connection = None

    def __init__(self, email, password):
        '''Login to vman and get a token'''
        url = 'http://www.virtualmanager.com/login'
        self.email = email
        self.password = password

        login_data = {'email': email, 'password': password}
        data = urllib.parse.urlencode(login_data)
        data = data.encode('utf-8')
        self.cookie = http.cookiejar.CookieJar()

        # http://stackoverflow.com/questions/2910221/how-can-i-login-to-a-website-with-python
        self.connection = urllib.request.build_opener(urllib.request.HTTPRedirectHandler(),
                                                      urllib.request.HTTPHandler(debuglevel=0),
                                                      urllib.request.HTTPSHandler(debuglevel=0),
                                                      urllib.request.HTTPCookieProcessor(self.cookie))
        self.connection.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                            'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]
        self.connection.open(url, data)


    def get_player_training(self, Player=None):
        if Player is None:
            return None

        url = Consts.URL['base'] + Consts.URL['player'] + Player.id + '-' + Player.firstName + '-' + Player.lastName + \
              Consts.URL['training']
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        responseData = response.read()
        print(responseData)

        return responseData

    def get_player_transfer_history(self, Player=None):
        if Player is None:
            return None

        url = Consts.URL['base'] + Consts.URL['player'] + Player.id + '-' + Player.firstName + '-' + Player.lastName + \
              Consts.URL['history']
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        responseData = response.read()

        return responseData

    def get_personal_info(self, Employee=None):
        if Employee is None:
            return None

        url = Consts.URL['base'] + Consts.URL['employee'] + Employee.id
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        responseData = response.read()

        return responseData

    def get_personal_search(self, role, page=1, min_age=0, max_age=99):
        if role is None:
            return None

        url = Consts.URL['base'] + Consts.URL['employee search'] + '&speciality=' + role + '&page=' + str(page)
        values = '&country_id=' + '&job_status=1' + '&age_min=' + str(min_age) + '&age_max='\
                 + str(max_age) + '&search=1&commit=S%C3%B8g'

        try:
            response = self.connection.open(url + values)
            responseData = response.read()
        except:
            responseData = '404'

        return responseData

    def get_player_information(self, Player=None):
        if Player is None:
            return None

        url = Consts.URL['base'] + Consts.URL['player'] + Player.id + '-' + Player.firstName + '-' + Player.lastName
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        response_data = response.read()
        return response_data


derp = RetrieverHTML('himmelherren@gmail.com', 'anders')
derp.get_personal_search('coach')

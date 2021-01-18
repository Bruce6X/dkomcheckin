import requests, re, sys

class checkin(object):
    def __init__(self, mainpage, i_number, email):
        self.mainpage = mainpage
        self.i_number = i_number
        self.email = email
        self.session = requests.session()

    def login(self):
        response = self.session.get(self.mainpage, verify=False)
        csrfmiddlewaretoken = re.findall(r"csrfmiddlewaretoken\" value=\"(.+?)\"", response.text)[0]
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': self.mainpage,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': self.mainpage,
        }
        data = {
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
            "uid": self.i_number,
            "email": self.email
        }
        response = self.session.post(self.mainpage+"/user/login/", headers=headers, data=data)

    def set_cookie(self):
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Referer': self.mainpage+"/",
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        params = (
            ('_callback', self.mainpage+'/center/api/public/index.php/v1/user/centerData/'),
        )
        response = self.session.get(self.mainpage+'/user/ajax-token-url/', headers=headers, params=params)
        t = re.findall(r"_t=(.+?)\"", response.text)[0]
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.mainpage,
            'Referer': self.mainpage+'/center/auth.html?_callback=https%3A%2F%2F' + self.mainpage[8:] + '%2Fcenter&_t={t}',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        data = {
          '_t': t,
          '_callback': 'https%3A%2F%2F'+self.mainpage[8:]+'%2Fcenter'
        }
        response = self.session.post(self.mainpage+'/center/api/public/index.php/v1/user/authAjax', headers=headers, data=data)

    def checkin(self):
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.mainpage,
            'Referer': self.mainpage+'/center/?_action=check_in',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        data = '{}'
        response = self.session.post(self.mainpage+"/center/api/public/index.php/v1/user/signIn", headers=headers, data=data).json()
        assert response['errcode'] == 200

    def do(self):
        self.login()
        self.set_cookie()
        self.checkin()

if __name__ == '__main__':
    obj = checkin(sys.argv[1], sys.argv[2], sys.argv[3])
    obj.do()
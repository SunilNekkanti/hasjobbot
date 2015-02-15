import mechanize
import re
from os import path
from sys import argv, exit
from lxml import etree

class Agent:
    _username = ''
    _password = ''
    _email= ''
    _phone = 0
    _message = """"""
    _keyword = ''

    def _configbot(self):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36"
        self._br.set_handle_robots(False)
        self._br.addheaders = [('User-agent', user_agent)]


    def __init__(self, data):
        self._username = data['username']
        self._password = data['password']
        self._phone = data['phone']
        self._email = data['email']
        self._message = data['message']
        self._keyword = data['keyword']
        self._br = mechanize.Browser()
        self._configbot()

    def _login(self, nr=1):
        self._br.open('http://hasjob.co/login')
        self._br.select_form(nr=nr)
        self._br['username'] = self._username
        self._br['password'] = self._password
        self._br.submit()
        return

    def _search_keyword(self, nr=0):
        self._br.open('http://hasjob.co')
        self._br.select_form(nr=nr)
        self._br['q'] = self._keyword
        self._br.submit()

    def _get_links(self):
        self._search_keyword(nr=0)
        links = [ l for l in self._br.links(url_regex=re.compile('/view/')) ]
        return links

    def _follow_links(self):
        for i, link in enumerate(self._get_links()):
            self._br.follow_link(link=link)
            self._submit_details(link)


    def _get_apply_form(self, link):
        try:
            link_follow = self._br.find_link(url_regex=re.compile('/reveal/'))
            self._br.follow_link(link=link_follow)
        except mechanize.LinkNotFoundError:
            pass
        return

    def _submit_details(self, link, nr=2):
        self._get_apply_form(link)
        try:
            self._br.select_form(nr=nr)
            self._br['apply_email'] = [self._email]
            self._br['apply_phone'] = self._phone
            self._br['apply_message'] = self._message
            self._br.submit()
        except mechanize.FormNotFoundError:
            pass
        return

    def apply(self):
        self._login()
        self._follow_links()

class Data:
    _data = {}
    _file = ''

    def __init__(self, path):
        self._file = open(path, 'r')

    def fromfile(self):
        root = etree.parse(self._file)
        data = {}
        for e in root.iter():
            if e.tag != 'user':
                data[e.tag] = e.text
        return data

    def validate(self, data):
        if 'username' and 'password' and 'email' and 'phone' and 'message' and 'keyword' in data:
            return True
        else:
            return False

def main():
    args = argv[1:]
    if not args:
        print('usage: [--dataFile] file.xml')
        exit(1)
    else:
        if args[0] == '--dataFile':
            file = args[1]
            if path.exists(file):
                data = Data(file)
                user_data = data.fromfile()
                if data.validate(user_data):
                    agnt = Agent(user_data)
                    agnt.apply()
                else:
                    print('ERROR: File is not containing enough data. Refer readme.txt')
            else:
                exit(1)
        else:
            print('usage: [--dataFile] file.xml')


if __name__ == '__main__':
    main()

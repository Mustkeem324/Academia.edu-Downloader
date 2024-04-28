import os
import re
import uuid
import sys
import requests
import json
from urllib.parse import urlparse

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def print_stylish_big(name):
    try:
        print("\033[92m" + name + "\033[0m")
    except Exception as eror:
        print(f"Error :{eror}")          

def generate_unique_token():
    try:
        token = uuid.uuid4().hex
        return token
    except Exception as eror:
        print(f"Error :{eror}")  

def download_document(url):
    try:
        payload = {}
        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'cookie': 'auvid=MTcxNDMzOTEzODk2NjowLjY3MDgyMDEzOTMxNzQ1MjM%3D; _ga=GA1.2.302615956.1714339144; user_id=68182943; cookie_test=68182943; admin_unrecorded_tests=%7B%22auth_system_version%22%3A%7B%22bucket%22%3A%22login_token_only%22%2C%22buckets%22%3A%5B%22y_cookie%22%2C%22login_token_only%22%5D%7D%7D; long_term_login=true; login_token=68182943%3Beae917443acadf80f6094636; ab_tests=%7B%22full_page_mobile_sutd_modal%22%3A%22control%22%2C%22mobile_view_tools_menu_fix_july_2023%22%3A%22control%22%2C%22remove_paper_claiming_from_upload_flow_june_2023_v1%22%3A%22control%22%7D; overridden_user_tests=%7B%22mobile_view_tools_menu_fix_july_2023%22%3A%22control%22%2C%22remove_paper_claiming_from_upload_flow_june_2023_v1%22%3A%22control%22%7D; _ga_5VKX33P2DS=GS1.2.1714339143.1.1.1714340177.47.0.0; request_id=jFbS6GXZ1ZjD9B7I0zQJ1TVPoB5PZOVU16SzufWe7hziiv9fh0sISg%3D%3D; ki_t=1714340179792%3B1714340179792%3B1714340179792%3B1%3B1; yauic=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaVkyT0RFNE1qazBNenRsWVdVNU1UYzBORE5oWTJGa1pqZ3daall3T1RRMk16WUdPZ1pGVkE9PSIsImV4cCI6IjIwMjUtMDQtMjhUMjE6MzY6MzYuNDc3WiIsInB1ciI6bnVsbH19--fb87b70c92f0b2276a051c3afc8d2ce8a55fe1f5; _cookie_session=MHVPWUl4dEQzNDV5eGF1cDVsYVRuTUZkaHM1UVZhYWlRUS91YkFiV0RXM2h1T3VySEx2a0FzKzdDLzlzQVkzejhlSWVEcWxGd1FsMEZjdTBIdVJIUWloNXcwLzBscEhTeXpsZ0RDa1ZWWmdtODNyQ2k1MFRSMnA4dUh5N3VvMFZhUkZ1ZDF0V1RFL0szd2g1OHA2TU43dmJCVFVzK0toNms4VkV4OUxOTkFkNFBHeVY1aVBRSFdlM0xoVDhtbkY4Y0VxZENCbHo2NjIyNnZhb0pnT0wyT0ExRXFpdWdzR0lTV2RiVjdmSi9XM0ZvNGU2dTVPQS9NZ2lDN21NTFl4enYzZVVvZjlJcks5ZHBEMzJqM1hYb2tFc1V2RytjdWlHUkpRVFRaY3kzYXB0RTV2dUJGTEFrampwVWxBNFN3YjhBMk9hc0hlS21idkI0aitrTGVaVXNCQUJ4MVV4dFlMZHNOV0VjWkFxZ1g1TlRMdnFTREh4aGh3UUVPMnM3TGZlNTJxZE8xTmtWa3EyblF5cUVhbzJzWWNiOW1vSGF3SXBDejlNSlJKSWRlMkoyVzZIRzZhUTBOMmx3ZUYvVzNjRTlmNWRpZEIxUUZncWVNZXR2T3MvQ3gzd0M0MzRpUUVJQnRCNkYrSCtVZVMvTDhzQWUyWmR3Ty83akxyRmhLY2hQQkZnN1N5QzRaMEw3V3A0OUR6cWZjZ0hjMi9IOTc1NTY0WVNSNmFES0lWejhqdTdDYjJkQ0p2NHJmMG5vZktCY2tDb2podmxka1NmaytONDRpR2ZVVWVBN1gyOVJFdHZSTG5SN0o1S3NoTmd6Ri9IUE5PbXFsWkJpZXlZOTBwWXVjUHd4TDRQSXp5RE9ZMGdpM2VVMmg1c2FheTZjL25qV3EvWkxYVkI1UEZaeXI0VjMrN1poU1ZXY2c3K2t4bm04MjE5YktQSmU5cFlkczBtR1lYMWt2MGFhV1dTaythTWU1cnZ1R01jOFNmM2cxQVJFVURwRVJPT1o3UXlXTHovRENLQ05tdlljeGNiQXRiSWcyYUpWbk9nbzkvUXB1cWNpbjlsVS9DamJwZElhZzNLMUNZOVBRdUl2cXV3QlIrTUVWRnU5eG9PSWprSHBnREl4SGxDOEVHK2pSMWhnNE82OW1SMW9LTE43UWtXUlFsb3VBRFNvWnFiWEdzZXFDZE8tLUVyOWEvakU0eWczc1dpMEM1YllPdVE9PQ%3D%3D--c882909c83b01d78c327a29cea25798512d2c264; request_id=CcLO0NtW7oemOdYAdA3t5Y3cuYOfnQ587APbl3CevYzwa_NUGyV4Eg%3D%3D; _cookie_session=M1BPR25BMnRoMWdlZWcrWHBTUEM1R1Ara3NGdDlpeHE0VUs3TkRZd0R5VG5qUjV4ZzcraEcwUUNjRVZEemoxMzhPbzRQY0I5RmVkNkUzQ2drVlIyRTdoVkE4K0dNV2NtbWFWQW1vUnhTcjlCbGxsUlJiTHBzeUlTZElESnJGQ2xLWkpoOERuUTQrVjI5Tk9nZnFoWEhoSFk4T0pyaWwyQ205U0RrUDUranRONE9CcUtvZnhYZEYwQWlNTjI4TGg1TnQyTFZhYjFJdUx5SnI1MDVweGpXTElxaVBER3N2ek5OMDVJU2dmZDNmTUt3a3E2VTRwYmgrZkx4b3QvZ2NLR0lUL09NN081YkxuNDlydnh6Vy9sVUl0MXRjTThrQXZrSHQ3a2VQN29BbnNxcjZDa3FWcE9MLzl3cVAyTkN3SFhkMEx6cHM5VGUzVnJhb0M4SE5GQ2JRSGZ3Tm5MaWZhc0E4V0oyYk5Ydm5xWVJWY0RRZzFmcTVsR0huSWppVDZucW42QitvV0dUYzkwQ0tEQVdGcjNmNlF6UnRub1RPWWtCMnNuWjFQRitBaVZhaHpOOGF1NWZ6SDBCR1IzdGllWWVYQVlQRHVHNExkSDBPOTkrQ0hESnRKYlFJbTNWclJBU3VucTNpWFZJczRqV3hMQk0wdUovMDlPT1VNaVhyMVNqQzRnQ3ZlaTRFNnZxSXo2S2FaVmNEMFdSMjZ5YWpaS202Y3J2bEJ3TXY4R1AxTmpRNWVsUDVwNzdlUG12czRtL0c4bVIwK29IMjhyNVVPQVJQaHJGY2hQdFRKd0pzZ3R0REkxbGRWTllqeGtSVkZOZW13T0JtMmdLYVVKWU53Y05NV1FycXJwUkpVUjBWVG1jdjM4RGNqSTNJSER0RHVlOFZGVElaaDZBMm9PZVBKT0ZoU2E2bXQreGxOeXJYNE5EKzJSREFsSjFGSDVJREpJY0t4U21sV0NrOERGWGY4VDNkNzF0Y0VWdDI0SERJR3hBT2pPU0hVdWluNVFGWnU5WjhreUlxUVdORG5GZytxVHk2LzdrRHptcjk2blJETjZRdVNBZjBuS2l0YXhoOGh6N0ZkWjYwWmRHTy9qRWIwUlR4cmovL1JacmdMRWJZeWkyM2RHelRNTGE4OTc3aFFWb21ScnhyRktJamNxaUZKemRZQjVCUkZ4MHZRNUl1ZlgtLUpySnNrSWJvdDVDdXE4b2FBL1pvNVE9PQ%3D%3D--27df343db811b24c3336fb388c8e2799aa50a683; admin_unrecorded_tests=%7B%22auth_system_version%22%3A%7B%22bucket%22%3A%22login_token_only%22%2C%22buckets%22%3A%5B%22y_cookie%22%2C%22login_token_only%22%5D%7D%7D; cookie_test=68182943; overridden_user_tests=%7B%22mobile_view_tools_menu_fix_july_2023%22%3A%22control%22%2C%22remove_paper_claiming_from_upload_flow_june_2023_v1%22%3A%22control%22%7D; user_id=68182943; yauic=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaVkyT0RFNE1qazBNenRsWVdVNU1UYzBORE5oWTJGa1pqZ3daall3T1RRMk16WUdPZ1pGVkE9PSIsImV4cCI6IjIwMjUtMDQtMjhUMjE6Mzc6NDEuMTg3WiIsInB1ciI6bnVsbH19--0f503df5abde2c9f9f4dbf9c28b4842c9b8f637e',
        'dnt': '1',
        'referer': 'https://www.academia.edu/search?q=matsh',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        print(f"Response Status:{response.status_code}" )
        if response.status_code == 200:
            pattern = r'bulkDownloadUrl&quot;:&quot;(.*?)&quot;'
            matches = re.findall(pattern, response.text)
            if matches:
                url = matches[0]
                # Replace '\u0026' with '&' using str.replace
                aurl = url.replace('\\u0026', '&')
                return aurl
            else:
                return None
        else:
            return 'Failed to fetch the page'
    except Exception as eror:
        print(f"Error :{eror}")    

 


if __name__ == "__main__":
    name ="""
                                                                                                              
                                                                                                          
NNNNNNNN        NNNNNNNXXXXXXX       XXXXXXX     PPPPPPPPPPPPPPPPP  RRRRRRRRRRRRRRRRR       OOOOOOOOO     
N:::::::N       N::::::X:::::X       X:::::X     P::::::::::::::::P R::::::::::::::::R    OO:::::::::OO   
N::::::::N      N::::::X:::::X       X:::::X     P::::::PPPPPP:::::PR::::::RRRRRR:::::R OO:::::::::::::OO 
N:::::::::N     N::::::X::::::X     X::::::X     PP:::::P     P:::::RR:::::R     R:::::O:::::::OOO:::::::O
N::::::::::N    N::::::XXX:::::X   X:::::XXX       P::::P     P:::::P R::::R     R:::::O::::::O   O::::::O
N:::::::::::N   N::::::N  X:::::X X:::::X          P::::P     P:::::P R::::R     R:::::O:::::O     O:::::O
N:::::::N::::N  N::::::N   X:::::X:::::X           P::::PPPPPP:::::P  R::::RRRRRR:::::RO:::::O     O:::::O
N::::::N N::::N N::::::N    X:::::::::X            P:::::::::::::PP   R:::::::::::::RR O:::::O     O:::::O
N::::::N  N::::N:::::::N    X:::::::::X            P::::PPPPPPPPP     R::::RRRRRR:::::RO:::::O     O:::::O
N::::::N   N:::::::::::N   X:::::X:::::X           P::::P             R::::R     R:::::O:::::O     O:::::O
N::::::N    N::::::::::N  X:::::X X:::::X          P::::P             R::::R     R:::::O:::::O     O:::::O
N::::::N     N:::::::::XXX:::::X   X:::::XXX       P::::P             R::::R     R:::::O::::::O   O::::::O
N::::::N      N::::::::X::::::X     X::::::X     PP::::::PP         RR:::::R     R:::::O:::::::OOO:::::::O
N::::::N       N:::::::X:::::X       X:::::X     P::::::::P         R::::::R     R:::::ROO:::::::::::::OO 
N::::::N        N::::::X:::::X       X:::::X     P::::::::P         R::::::R     R:::::R  OO:::::::::OO   
NNNNNNNN         NNNNNNXXXXXXX       XXXXXXX     PPPPPPPPPP         RRRRRRRR     RRRRRRR    OOOOOOOOO     
                                                                                                          
                                                                                                          
                                                                                                          
                                                                                                          
                                                                                                          
                                                                                                          
                                                                                                              
        """
    name2 ="""    _                _                 _
                        | |              (_)               | |
      __ _  ___ __ _  __| | ___ _ __ ___  _  __ _   ___  __| |_   _
     / _` |/ __/ _` |/ _` |/ _ \ '_ ` _ \| |/ _` | / _ \/ _` | | | |
    | (_| | (_| (_| | (_| |  __/ | | | | | | (_| ||  __/ (_| | |_| |
     \__,_|\___\__,_|\__,_|\___|_| |_| |_|_|\__,_(_)___|\__,_|\__,_|

        """   
    print_stylish_big(name)
    print_stylish_big(name2)
    link = input("Enter the Issuu document link: ")
    if link:
        print(f"Link Download: {link}")
        print("\033[92m" + link + "\033[0m")
        token = generate_unique_token()
        document_url = download_document(link)
        print(f"Document URL: {document_url}")
        if document_url:
            response = requests.get(document_url)
            if response.status_code == 200:
                document_content = response.content
                file_name = get_filename_from_url(document_url)
                with open(file_name, "wb") as document_file:
                    document_file.write(document_content)
                print("\033[92mDocument downloaded successfully\033[0m")
            else:
                print("Failed to download document")
        else:
            print("Invalid document URL")
    else:
        print("NO link")

    

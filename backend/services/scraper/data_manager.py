import requests


class ScrapperDataManager:
    def __init__(self) -> None:
        self.url = "https://kargo-ucreti.hesaplama.net/"
        self.set_cities()
        self.set_session()
        self.set_headers()
        self.set_cookies()
        
    def set_session(self) -> None:
        self.session = requests.Session()
        
    def set_headers(self) -> None:
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,tr-TR;q=0.6,tr;q=0.5",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "dnt": "1",
            "origin": "https://kargo-ucreti.hesaplama.net",
            "priority": "u=0, i",
            "referer": "https://kargo-ucreti.hesaplama.net/",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        
    def set_cookies(self) -> None:
        self.cookies = {
            "__gads": "ID=e64aa514dae7e3c4:T=1725280571:RT=1725280571:S=ALNI_MZpxR8HE6TQm9a4kd5bMG-lqqJk-A",
            "__gpi": "UID=00000eb601040a06:T=1725280571:RT=1725280571:S=ALNI_MbIsrlVhCe_O_bC0wIw3LiLrnyM0g",
            "__eoi": "ID=6beb083dc8311cd4:T=1725280571:RT=1725280571:S=AA-AfjZRdUam3Nq0OYych6fuAwrP",
            "_hnvcv": "2",
            "_hnvid": "14f87931-2221-4006-8000-df0bb67a4186",
            "_hnvcs": "cf688343",
            "_ga": "GA1.1.1576733802.1731000700",
            "PHPSESSID": "23c7g8siib5810vjseu9gp39os",
            "_hnvsur": "1",
            "FCNEC": "%5B%5B%22AKsRol_QMxKbFjJIaDuwixuWihFqkURCioyMiSmSgiFOBJJyjmO7B8h5IXyZC1WBBaOYGv9ac0NE-87cieGnyVOjhtAksh6Z0Jk-sVfkfthI4UW08HbOeDmc6FiXwSfE2AKGlQEiZnSzAMtt8rfViFEajHfaRpLS6Q%3D%3D%22%5D%5D",
            "_ga_7VKF8CJQ50": "GS1.1.1731000699.1.1.1731004285.54.0.998352356"
        }
    
    def set_cities(self) -> None:
        self.cities = {
            "adana": 1,
            "adıyaman": 2,
            "afyon": 3,
            "ağrı": 4,
            "aksaray": 68,
            "amasya": 5,
            "ankara": 6,
            "antalya": 7,
            "ardahan": 75,
            "artvin": 8,
            "aydın": 9,
            "balıkesir": 10,
            "bartın": 74,
            "batman": 72,
            "bayburt": 69,
            "bilecik": 11,
            "bingöl": 12,
            "bitlis": 13,
            "bolu": 14,
            "burdur": 15,
            "bursa": 16,
            "çanakkale": 17,
            "çankırı": 18,
            "çorum": 19,
            "denizli": 20,
            "diyarbakır": 21,
            "düzce": 81,
            "edirne": 22,
            "elazığ": 23,
            "erzincan": 24,
            "erzurum": 25,
            "eskişehir": 26,
            "gaziantep": 27,
            "giresun": 28,
            "gümüşhane": 29,
            "hakkari": 30,
            "hatay": 31,
            "ığdır": 76,
            "ısparta": 32,
            "içel": 33,
            "istanbul": 34,
            "izmir": 35,
            "kahramanmaraş": 46,
            "karabük": 78,
            "karaman": 70,
            "kars": 36,
            "kastamonu": 37,
            "kayseri": 38,
            "kırıkkale": 71,
            "kırklareli": 39,
            "kırşehir": 40,
            "kilis": 79,
            "kocaeli": 41,
            "konya": 42,
            "kütahya": 43,
            "malatya": 44,
            "manisa": 45,
            "mardin": 47,
            "muğla": 48,
            "muş": 49,
            "nevşehir": 50,
            "niğde": 51,
            "ordu": 52,
            "osmaniye": 80,
            "rize": 53,
            "sakarya": 54,
            "samsun": 55,
            "siirt": 56,
            "sinop": 57,
            "sivas": 58,
            "şanlıurfa": 63,
            "şırnak": 73,
            "tekirdağ": 59,
            "tokat": 60,
            "trabzon": 61,
            "tunceli": 62,
            "uşak": 64,
            "van": 65,
            "yalova": 77,
            "yozgat": 66,
            "zonguldak": 67
        }


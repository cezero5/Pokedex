from core.PokedexImport import requests


BASE_URL = "https://pokeapi.co/api/v2/"


# ----------------- 1) Requests: SOLO IO/RED -----------------
class PokeApiClient:
    def __init__(self, base_url=BASE_URL, timeout=20):
        self.base_url = base_url
        self.timeout = timeout

    def list_pokemon_names(self, limit=1302):
        data = requests.get(self.base_url + f"pokemon?limit={limit}", timeout=self.timeout).json()
        return [p["name"] for p in data.get("results", [])]

    def list_move_names(self, limit=937):
        data = requests.get(self.base_url + f"move?limit={limit}", timeout=self.timeout).json()
        return [m["name"] for m in data.get("results", [])]

    def get_pokemon(self, name: str):
        return requests.get(self.base_url + f"pokemon/{name}", timeout=self.timeout).json()
    
    def get_move(self, name: str):
        return requests.get(self.base_url + f"move/{name}", timeout=self.timeout).json()
    
    def get_species(self, name: str):
        return requests.get(self.base_url + f"pokemon-species/{name}", timeout=self.timeout).json()
    
    def get_image_bytes(self, url: str):
        return requests.get(url, timeout=self.timeout).content

from agno.tools import tool
import requests

@tool
def getProgramBrofesional():
    """Mengambil data program dari API Brofesional dengan kategori 'lainnya' halaman 1"""
    url = "https://franken-api.brofesional.id/api/feature/membership/main-program"
    params = {"filter[category.slug]": "lainnya", "page": 1}
    response = requests.get(url, params=params)
    return response.json()

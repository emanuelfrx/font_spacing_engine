import os
import requests

def download_google_font(font_name, api_key, output_dir="data/raw"):
    """
    Busca e baixa o arquivo .ttf da fonte diretamente da Google Fonts API.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = f"{output_dir}/{font_name.replace(' ', '')}-Regular.ttf"
    
    # Se a fonte já foi baixada anteriormente, pula o download
    if os.path.exists(file_path):
        print(f"[~] Fonte {font_name} já existe localmente.")
        return file_path

    # URL da API do Google Web Fonts
    api_url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={api_key}&family={font_name.replace(' ', '+')}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        # Pega a URL da variante 'regular' (peso 400)
        font_url = data['items'][0]['files'].get('regular')
        
        if not font_url:
            print(f"[!] Variante 'regular' não encontrada para {font_name}.")
            return None
            
        # Força o download do formato .ttf (o Google costuma servir woff2 por padrão em web)
        font_data = requests.get(font_url)
        
        with open(file_path, "wb") as f:
            f.write(font_data.content)
            
        print(f"[*] Fonte {font_name} baixada com sucesso.")
        return file_path

    except Exception as e:
        print(f"[!] Falha ao baixar {font_name}: {e}")
        return None
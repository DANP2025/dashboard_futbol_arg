import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_todays_matches():
    """
    Obtiene los partidos de hoy de las ligas de Argentina usando API-Football de RapidAPI.
    Ligas: Liga Profesional (ID 128), Primera Nacional (ID 129), Federal A (ID 130)
    
    Returns:
        pd.DataFrame: DataFrame con columnas Liga, Hora, Local, Visitante, Resultado
    """
    
    # Obtener API Key desde .env
    api_key = os.getenv('RAPIDAPI_KEY')
    
    if not api_key:
        raise ValueError("No se encontró RAPIDAPI_KEY en el archivo .env")
    
    # Configuración de la API
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    
    # Obtener fecha de hoy en formato YYYY-MM-DD
    today = datetime.now().strftime('%Y-%m-%d')
    
    # IDs de las ligas argentinas
    league_ids = {
        128: 'Liga Profesional',
        129: 'Primera Nacional',
        130: 'Federal A'
    }
    
    all_matches = []
    
    # Hacer una llamada por cada liga
    for league_id, league_name in league_ids.items():
        params = {
            "date": today,
            "league": league_id,
            "season": 2025  # Ajustar según la temporada actual
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('response'):
                for match in data['response']:
                    match['league_name'] = league_name
                all_matches.extend(data['response'])
                
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener partidos de la liga {league_id}: {e}")
            continue
    
    # Procesar los datos
    matches_data = []
    
    for match in all_matches:
        # Extraer información básica
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        
        # Extraer hora
        fixture_date = match['fixture']['date']
        hour = datetime.fromisoformat(fixture_date.replace('Z', '+00:00')).strftime('%H:%M')
        
        # Extraer resultado
        if match['fixture']['status']['short'] == 'NS':
            result = 'No jugado'
        elif match['fixture']['status']['short'] == 'LIVE':
            result = f"{match['goals']['home']} - {match['goals']['away']} (En vivo)"
        elif match['fixture']['status']['short'] == 'FT':
            result = f"{match['goals']['home']} - {match['goals']['away']}"
        elif match['fixture']['status']['short'] == 'HT':
            result = f"{match['goals']['home']} - {match['goals']['away']} (Entretiempo)"
        else:
            result = match['fixture']['status']['long']
        
        matches_data.append({
            'Liga': match['league_name'],
            'Hora': hour,
            'Local': home_team,
            'Visitante': away_team,
            'Resultado': result
        })
    
    # Crear DataFrame
    df = pd.DataFrame(matches_data)
    
    # Ordenar por hora
    df = df.sort_values('Hora')
    
    return df

if __name__ == "__main__":
    # Prueba de la función
    try:
        df = get_todays_matches()
        print("Partidos de hoy:")
        print(df.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")

import re
import json
import httpx

def extract_json_from_embed(html):
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
    return json.loads(match.group(1)) if match else None

async def get_track_info(track_id):
    embed_url = f"https://open.spotify.com/embed/track/{track_id}?utm_source=fxspotify"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(embed_url, headers=headers)
            response.raise_for_status()
            json_data = extract_json_from_embed(response.text)
            if not json_data:
                return {"error": "Failed to extract track data"}
            
            entity = json_data.get('props', {}).get('pageProps', {}).get('state', {}).get('data', {}).get('entity', {})
            if not entity:
                return {"error": "No entity data found"}
            
            images = entity.get('visualIdentity', {}).get('image', [])
            sorted_images = sorted(images, key=lambda x: x.get('maxWidth', 0), reverse=True)
            
            return {
                'name': entity.get('name'),
                'artists': [{'name': a.get('name'), 'uri': a.get('uri')} for a in entity.get('artists', [])],
                'audio_preview_url': entity.get('audioPreview', {}).get('url'),
                'album': {
                    'images': [{'url': img.get('url'), 'height': img.get('maxHeight'), 'width': img.get('maxWidth')} 
                               for img in sorted_images],
                    'release_date': entity.get('releaseDate', {}).get('isoString')
                },
                'duration': entity.get('duration'),
                'external_urls': {'spotify': f"https://open.spotify.com/track/{track_id}"}
            }
        except httpx.HTTPError:
            return {"error": "Failed to get track info"}
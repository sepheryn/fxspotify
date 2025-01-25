from quart import Blueprint, jsonify, request
from services.track_service import get_track_info

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/track/<track_id>')
async def track_api(track_id):
    return jsonify(await get_track_info(track_id))

@api_bp.route('/oembed.json')
async def oembed():
    track_id = request.args.get('id')
    if not track_id:
        return jsonify({"error": "Missing track ID"}), 400
    
    track_info = await get_track_info(track_id)
    if 'error' in track_info:
        return jsonify({"error": "Track not found"}), 404
    
    artists = [a['name'] for a in track_info['artists']]
    artists_str = ', '.join(artists[:-1] + [' and ' + artists[-1]] if len(artists) > 1 else artists)
    author_url = f"https://open.spotify.com/artist/{track_info['artists'][0]['uri'].split(':')[-1]}" if track_info['artists'] else ""
    
    oembed_data = {
        "type": "rich",
        "version": "1.0",
        "title": track_info['name'],
        "provider_name": "FxSpotify",
        "provider_url": "https://fxspotify.com/",
        "author_name": artists_str,
        "author_url": author_url,
        "width": track_info['album']['images'][0]['width'] if track_info['album']['images'] else 640,
        "height": track_info['album']['images'][0]['height'] if track_info['album']['images'] else 640,
        "thumbnail_url": track_info['album']['images'][0]['url'] if track_info['album']['images'] else "",
        "html": f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{track_id}?utm_source=fxspotify" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
    }
    
    if track_info.get('audio_preview_url'):
        oembed_data['audio_url'] = track_info['audio_preview_url']
    
    return jsonify(oembed_data)
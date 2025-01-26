from quart import Blueprint, render_template, request   
from services.track_service import get_track_info

track_bp = Blueprint('track', __name__)

@track_bp.route('/track/<track_id>', defaults={'intl_part': None})
@track_bp.route('/<intl_part>/track/<track_id>')
async def track_page(intl_part, track_id):
    track_info = await get_track_info(track_id)
    if 'error' in track_info:
        return await render_template('error.html')   
    
    preview_url = track_info.get('audio_preview_url')
    artists = [artist['name'] for artist in track_info['artists']]
    artists_str = ', '.join(artists[:-1] + [' and ' + artists[-1]] if len(artists) > 1 else artists)
    description = f"Song · {artists_str}" if preview_url else "Preview not available."
    
    return await render_template(
        'track.html',
        track_info=track_info,
        track_id=track_id,
        artists_string=artists_str,
        preview_url=preview_url,
        description=description
    )
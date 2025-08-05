from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MOVIE_UPDATE_CHANNEL = -1002544936859

# This function can be called wherever you add a new movie to your DB/storage.
async def send_movie_update(client: Client, movie: dict):
    """
    movie dict keys: title, year, poster_url, imdb_url, plot, etc.
    """
    caption = (
        f"<b>🎬 New Movie Added!</b>\n"
        f"<b>Title:</b> {movie.get('title')}\n"
        f"<b>Year:</b> {movie.get('year', 'N/A')}\n"
        f"<b>Plot:</b> {movie.get('plot', 'No plot available')}\n"
        f"<b>IMDB:</b> <a href='{movie.get('imdb_url', '')}'>Link</a>"
    )
    buttons = [
        [InlineKeyboardButton("Watch Trailer", url=movie.get("trailer_url", "https://imdb.com"))]
    ]
    try:
        await client.send_photo(
            MOVIE_UPDATE_CHANNEL,
            photo=movie.get("poster_url"),
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html"
        )
    except Exception as e:
        await client.send_message(
            MOVIE_UPDATE_CHANNEL,
            caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html"
        )
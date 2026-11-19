# MovieBox API MCP Server

MCP server wrapping the Movie Release Tracker and TuneFind Tracker APIs, exposing them as tools for AI agents (Claude, Cursor, OpenCode).

## Tools

### Movie Release Tracker
- `release_tracker_health` — API health check
- `search_movies` — search by title, IMDb ID, or year
- `get_movie_by_imdb` — look up movie by IMDb ID
- `get_movie_releases` — DVD/Blu-ray/4K/digital releases for a movie
- `get_releases` — list releases with filters
- `get_upcoming_releases` — upcoming releases (7/30/60 day window)
- `get_release_calendar` — monthly release calendar
- `lookup_release_by_upc` — UPC barcode lookup
- `lookup_release_by_asin` — ASIN lookup

### TuneFind Tracker
- `tunefind_health` — API health check
- `parse_tunefind_episode` — parse a TuneFind episode page (songs, artists, scenes)
- `search_tunefind_songs` — search songs by title
- `list_tunefind_shows` — list all shows
- `get_tunefind_show` — get show by ID
- `get_tunefind_show_episodes` — get all episodes + songs for a show
- `get_tunefind_artists` — list/filter artists
- `get_tunefind_song_placements` — where a song appears

## Setup

```bash
cd ~/api-mcp-server
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Register in OpenCode

Add to `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "moviebox-apis": {
      "type": "local",
      "command": ["/home/alen/api-mcp-server/.venv/bin/python", "/home/alen/api-mcp-server/mcp_server.py"]
    }
  }
}
```

## Verify it works

After restarting OpenCode, you should see 17 tools available under the `moviebox-apis` namespace. Test with:

```
Search for movies with "Dune" in the title
Get upcoming digital releases for the next 30 days
Parse the TuneFind page for Breaking Bad S1E1
```

## Run manually

```bash
.venv/bin/python mcp_server.py
```
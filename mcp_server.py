"""MCP server wrapping Movie Release Tracker and TuneFind Tracker APIs."""
import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("moviebox-apis")

RELEASE_TRACKER_URL = "https://digital-release-tracker-nocap3.vercel.app"
TUNEFIND_TRACKER_URL = "https://tunefind-tracker.vercel.app"


# ── Movie Release Tracker tools ──────────────────────────────────────

@mcp.tool()
def release_tracker_health() -> str:
    """Check if the Movie Release Tracker API is healthy and connected to its database."""
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/health", timeout=15)
    return resp.text


@mcp.tool()
def search_movies(title: str = None, imdb_id: str = None, release_year: int = None) -> str:
    """Search movies in the release tracker database.

    Args:
        title: Case-insensitive title substring search.
        imdb_id: Exact IMDb ID (e.g. tt21097228).
        release_year: Filter by primary release year.
    """
    params = {}
    if title:
        params["title"] = title
    if imdb_id:
        params["imdb_id"] = imdb_id
    if release_year:
        params["release_year"] = release_year
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/movies", params=params, timeout=15)
    return resp.text


@mcp.tool()
def get_movie_by_imdb(imdb_id: str) -> str:
    """Look up a movie by its IMDb ID (e.g. tt21097228)."""
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/movies/imdb/{imdb_id}", timeout=15)
    return resp.text


@mcp.tool()
def get_movie_releases(movie_id: int, format: str = None, status: str = None) -> str:
    """Get DVD/Blu-ray/4K/digital release dates for a movie by its internal ID.

    Args:
        movie_id: Internal movie ID from the release tracker.
        format: Filter by format: dvd, blu_ray, 4k_uhd, or digital.
        status: Filter by status: announced, released, postponed, etc.
    """
    params = {}
    if format:
        params["format"] = format
    if status:
        params["status"] = status
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/movies/{movie_id}/releases", params=params, timeout=15)
    return resp.text


@mcp.tool()
def get_releases(format: str = None, status: str = None, start_date: str = None, end_date: str = None, limit: int = 20) -> str:
    """List/paginate releases with optional filters.

    Args:
        format: dvd, blu_ray, 4k_uhd, or digital.
        status: announced, released, postponed, unannounced, cancelled, unknown.
        start_date: Releases on or after (YYYY-MM-DD).
        end_date: Releases on or before (YYYY-MM-DD).
        limit: Max results (1-100, default 20).
    """
    params = {"limit": limit}
    if format:
        params["format"] = format
    if status:
        params["status"] = status
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/releases", params=params, timeout=15)
    return resp.text


@mcp.tool()
def get_upcoming_releases(window_days: int = 30, format: str = None) -> str:
    """Get upcoming movie releases within a window (7, 30, or 60 days).

    Args:
        window_days: Window size in days (7, 30, or 60). Default 30.
        format: Filter by format: dvd, blu_ray, 4k_uhd, or digital.
    """
    params = {"window_days": window_days}
    if format:
        params["format"] = format
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/releases/upcoming", params=params, timeout=15)
    return resp.text


@mcp.tool()
def get_release_calendar(year: int, month: int) -> str:
    """Get the monthly release calendar for a given month.

    Args:
        year: Four-digit year (e.g. 2026).
        month: Month (1-12).
    """
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/releases/calendar/{year}/{month}", timeout=15)
    return resp.text


@mcp.tool()
def lookup_release_by_upc(upc: str) -> str:
    """Look up a release by its 12-digit UPC barcode."""
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/releases/upc/{upc}", timeout=15)
    return resp.text


@mcp.tool()
def lookup_release_by_asin(asin: str) -> str:
    """Look up a release by its 10-character Amazon ASIN."""
    resp = httpx.get(f"{RELEASE_TRACKER_URL}/api/v1/releases/asin/{asin}", timeout=15)
    return resp.text


# ── TuneFind Tracker tools ───────────────────────────────────────────

@mcp.tool()
def tunefind_health() -> str:
    """Check if the TuneFind Tracker API is healthy."""
    resp = httpx.get(f"{TUNEFIND_TRACKER_URL}/health", timeout=15)
    return resp.text


@mcp.tool()
def parse_tunefind_episode(url: str) -> str:
    """Fetch and parse a TuneFind episode page, returning songs, artists, scene descriptions, and metadata.

    Args:
        url: Full TuneFind episode URL (e.g. https://www.tunefind.com/show/breaking-bad/season-1/8288).
    """
    resp = httpx.get(f"{TUNEFIND_TRACKER_URL}/api/v1/episodes/parse", params={"url": url}, timeout=30)
    return resp.text


@mcp.tool()
def search_tunefind_songs(query: str) -> str:
    """Search songs by title in the TuneFind database.

    Args:
        query: Song title search term.
    """
    resp = httpx.get(f"{TUNEFIND_TRACKER_URL}/api/v1/songs/search", params={"q": query}, timeout=15)
    return resp.text


@mcp.tool()
def list_tunefind_shows() -> str:
    """List all shows in the TuneFind database."""
    resp = httpx.get(f"{TUNEFIND_TRACKER_URL}/api/v1/shows", timeout=15)
    return resp.text


@mcp.tool()
def get_tunefind_show(show_id: int) -> str:
    """Get a show by its internal ID.

    Args:
        show_id: Internal show ID.
    """
    resp = httpx.get(f"{TUNEFIND_TRACKER_URL}/api/v1/shows/{show_id}", timeout=15)
    return resp.text


@mcp.tool()
def get_tunefind_show_episodes(show_id: int) -> str:
    """Get all episodes for a show, including songs and scene descriptions.

    Args:
        show_id: Internal show ID.
    """
    resp = httpx.get(f"{TUNEFIND_TRACKER_URL}/api/v1/shows/{show_id}/episodes", timeout=15)
    return resp.text


@mcp.tool()
def get_tunefind_artists(name: str = None) -> str:
    """List artists in the TuneFind database, optionally filtered by name.

    Args:
        name: Case-insensitive name substring search.
    """
    params = {}
    if name:
        params["name"] = name
    resp = httpx.get(f"{TUNEFIND_TRACKER_URL}/api/v1/artists", params=params, timeout=15)
    return resp.text


@mcp.tool()
def get_tunefind_song_placements(song_id: int) -> str:
    """Get all placements (episodes) where a song appears.

    Args:
        song_id: Internal song ID.
    """
    resp = httpx.get(f"{TUNEFIND_TRACKER_URL}/api/v1/songs/{song_id}/placements", timeout=15)
    return resp.text


def main():
    mcp.run()


if __name__ == "__main__":
    main()
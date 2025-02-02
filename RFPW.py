import yaml
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
from urllib.parse import urlparse
from plexapi.exceptions import BadRequest

def print_progress(current, total, prefix=""):
    percent = current / total * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r{prefix} |{bar}| {percent:.1f}% ({current}/{total})', end='', flush=True)
    if current == total:
        print()

def extract_tmdb_id(item):
    for guid in item.guids:
        parsed = urlparse(guid.id)
        if parsed.scheme == 'tmdb':
            return int(parsed.netloc)
    return None

def extract_tvdb_id(item):
    for guid in item.guids:
        parsed = urlparse(guid.id)
        if parsed.scheme == 'tvdb':
            return int(parsed.netloc)
    return None

def main():
    with open('config.yml') as f:
        config = yaml.safe_load(f)

    # Connect to Plex
    plex = PlexServer(config['plex_url'], config['plex_api_key'])
    account = MyPlexAccount(token=config['plex_api_key'])

    # Initialize lists
    movies_to_remove = []
    tv_shows_to_remove = []
    movies_in_watchlist = []
    tv_in_watchlist = []

    # Get watchlist items with progress
    if config['check_movies']:
        print("Fetching movie watchlist...")
        movie_watchlist = list(account.watchlist(libtype='movie'))
        total = len(movie_watchlist)
        for index, item in enumerate(movie_watchlist, 1):
            if tmdb_id := extract_tmdb_id(item):
                movies_in_watchlist.append({'id': tmdb_id, 'item': item})
            print_progress(index, total, "Fetching movie watchlist")
        print()

    if config['check_tv_shows']:
        print("Fetching TV show watchlist...")
        tv_watchlist = list(account.watchlist(libtype='show'))
        total = len(tv_watchlist)
        for index, item in enumerate(tv_watchlist, 1):
            if tvdb_id := extract_tvdb_id(item):
                tv_in_watchlist.append({'id': tvdb_id, 'item': item})
            print_progress(index, total, "Fetching TV watchlist")
        print()

    # Process libraries with progress
    if config['check_movies']:
        movie_library = plex.library.section(config['movie_library_name'])
        total = movie_library.totalSize
        print(f"Scanning {total} movies in library...")
        for index, movie in enumerate(movie_library.all(), 1):
            if movie.viewCount > 0:
                if tmdb_id := extract_tmdb_id(movie):
                    if tmdb_id in [m['id'] for m in movies_in_watchlist]:
                        movies_to_remove.append({
                            'title': movie.title,
                            'year': movie.year,
                            'id': tmdb_id
                        })
            print_progress(index, total, "Processing movies")
        print()

    if config['check_tv_shows']:
        tv_library = plex.library.section(config['tv_library_name'])
        total = tv_library.totalSize
        print(f"Scanning {total} TV shows in library...")
        for index, show in enumerate(tv_library.all(), 1):
            if hasattr(show, 'viewedLeafCount') and hasattr(show, 'leafCount'):
                if show.viewedLeafCount == show.leafCount:
                    if tvdb_id := extract_tvdb_id(show):
                        if tvdb_id in [t['id'] for t in tv_in_watchlist]:
                            tv_shows_to_remove.append({
                                'title': show.title,
                                'year': show.year,
                                'id': tvdb_id
                            })
            print_progress(index, total, "Processing TV shows")
        print()

    # Display results
    if config['check_movies']:
        if movies_to_remove:
            print("Watched Movies in Watchlist:")
            for movie in movies_to_remove:
                print(f" - {movie['title']} ({movie['year']})")
        else:
            print("No watched movies found in watchlist")
    
    if config['check_tv_shows']:
        print()
        if tv_shows_to_remove:
            print("Watched TV Shows in Watchlist:")
            for show in tv_shows_to_remove:
                print(f" - {show['title']} ({show['year']})")
        else:
            print("No watched TV shows found in watchlist")

    # Remove from watchlist
    if config['remove_from_watchlist']:
        # Process movies removal
        movie_ids = {m['id'] for m in movies_to_remove}
        to_remove_movies = [wl for wl in movies_in_watchlist if wl['id'] in movie_ids]
        if to_remove_movies:
            total = len(to_remove_movies)
            print(f"\nRemoving {total} movies from watchlist...")
            for index, item in enumerate(to_remove_movies, 1):
                try:
                    account.removeFromWatchlist(item['item'])
                except BadRequest as e:
                    print(f"\n  ⚠️  Skipping: {item['item'].title} was already removed from watchlist")
                print_progress(index, total, "Removing movies")
            print()

        # Process TV shows removal
        tv_ids = {t['id'] for t in tv_shows_to_remove}
        to_remove_tv = [wl for wl in tv_in_watchlist if wl['id'] in tv_ids]
        if to_remove_tv:
            total = len(to_remove_tv)
            print(f"Removing {total} TV shows from watchlist...")
            for index, item in enumerate(to_remove_tv, 1):
                try:
                    account.removeFromWatchlist(item['item'])
                except BadRequest as e:
                    print(f"\n  ⚠️  Skipping: {item['item'].title} was already removed from watchlist")
                print_progress(index, total, "Removing TV shows")
            print()

if __name__ == '__main__':
    main()
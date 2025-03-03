import yaml
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
from urllib.parse import urlparse
from plexapi.exceptions import BadRequest, Unauthorized

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

def process_user_watchlist(account, plex, config, username="Admin"):
    # Initialize lists
    movies_to_remove = []
    tv_shows_to_remove = []
    movies_in_watchlist = []
    tv_in_watchlist = []

    # Get watchlist items with progress
    if config['check_movies']:
        print(f"\nFetching movie watchlist for {username}...")
        try:
            movie_watchlist = list(account.watchlist(libtype='movie'))
            total = len(movie_watchlist)
            for index, item in enumerate(movie_watchlist, 1):
                if tmdb_id := extract_tmdb_id(item):
                    movies_in_watchlist.append({'id': tmdb_id, 'item': item})
                print_progress(index, total, f"Processing")
            print()
        except Exception as e:
            print(f"Error fetching movie watchlist for {username}: {str(e)}")
            movie_watchlist = []

    if config['check_tv_shows']:
        print(f"Fetching TV show watchlist for {username}...")
        try:
            tv_watchlist = list(account.watchlist(libtype='show'))
            total = len(tv_watchlist)
            for index, item in enumerate(tv_watchlist, 1):
                if tvdb_id := extract_tvdb_id(item):
                    tv_in_watchlist.append({'id': tvdb_id, 'item': item})
                print_progress(index, total, f"Processing")
            print()
        except Exception as e:
            print(f"Error fetching TV watchlist for {username}: {str(e)}")
            tv_watchlist = []

    # For external users, we need to get their watched status directly from their account
    if username != "Admin":
        try:
            # Get the user's resources (servers they have access to)
            user_resources = account.resources()
            user_server = None
            
            # Find the server that matches our current server
            for resource in user_resources:
                if resource.name == plex.friendlyName or resource.clientIdentifier == plex.machineIdentifier:
                    user_server = resource
                    break
            
            if user_server:
                print(f"Found matching server in {username}'s resources")
                # Connect to the server with the user's token
                user_plex = user_server.connect()
                print(f"Connected to Plex as {username} for accurate watch status")
            else:
                print(f"⚠️ Could not find matching server in {username}'s resources")
                print(f"⚠️ Skipping watch status check for {username}")
                return 0, 0
        except Exception as e:
            print(f"⚠️ Error connecting to Plex as {username}: {str(e)}")
            print(f"⚠️ Skipping watch status check for {username}")
            return 0, 0
    else:
        user_plex = plex

    # Process libraries with progress
    if config['check_movies']:
        try:
            movie_library = user_plex.library.section(config['movie_library_name'])
            total = movie_library.totalSize
            print(f"Scanning {total} movies in library for {username}...")
            for index, movie in enumerate(movie_library.all(), 1):
                # When using user's own connection, viewCount will be accurate for them
                if movie.viewCount > 0:
                    if tmdb_id := extract_tmdb_id(movie):
                        if tmdb_id in [m['id'] for m in movies_in_watchlist]:
                            movies_to_remove.append({
                                'title': movie.title,
                                'year': movie.year,
                                'id': tmdb_id
                            })
                        
                print_progress(index, total, f"Processing")
            print()
        except Exception as e:
            print(f"⚠️ Error accessing movie library for {username}: {str(e)}")

    if config['check_tv_shows']:
        try:
            tv_library = user_plex.library.section(config['tv_library_name'])
            total = tv_library.totalSize
            print(f"Scanning {total} TV shows in library for {username}...")
            for index, show in enumerate(tv_library.all(), 1):
                # When using user's own connection, viewedLeafCount will be accurate for them
                if hasattr(show, 'viewedLeafCount') and hasattr(show, 'leafCount'):
                    if show.viewedLeafCount == show.leafCount and show.leafCount > 0:
                        if tvdb_id := extract_tvdb_id(show):
                            if tvdb_id in [t['id'] for t in tv_in_watchlist]:
                                tv_shows_to_remove.append({
                                    'title': show.title,
                                    'year': show.year,
                                    'id': tvdb_id
                                })
                        
                print_progress(index, total, f"Processing")
            print()
        except Exception as e:
            print(f"⚠️ Error accessing TV library for {username}: {str(e)}")

    # Display results
    if config['check_movies']:
        if movies_to_remove:
            print(f"Watched Movies in {username}'s Watchlist:")
            for movie in movies_to_remove:
                print(f" - {movie['title']} ({movie['year']})")
        else:
            print(f"No watched movies found in {username}'s watchlist")
    
    if config['check_tv_shows']:
        print()
        if tv_shows_to_remove:
            print(f"Watched TV Shows in {username}'s Watchlist:")
            for show in tv_shows_to_remove:
                print(f" - {show['title']} ({show['year']})")
        else:
            print(f"No watched TV shows found in {username}'s watchlist")

    # Remove from watchlist
    movies_removed = 0
    shows_removed = 0
    
    if config['remove_from_watchlist']:
        # Process movies removal
        movie_ids = {m['id'] for m in movies_to_remove}
        to_remove_movies = [wl for wl in movies_in_watchlist if wl['id'] in movie_ids]
        if to_remove_movies:
            total = len(to_remove_movies)
            movies_removed = total
            print(f"\nRemoving {total} movies from {username}'s watchlist...")
            for index, item in enumerate(to_remove_movies, 1):
                try:
                    account.removeFromWatchlist(item['item'])
                except BadRequest as e:
                    print(f"\n  ⚠️  Skipping: {item['item'].title} was already removed from {username}'s watchlist")
                print_progress(index, total, f"Removing movies from {username}'s watchlist")
            print()

        # Process TV shows removal
        tv_ids = {t['id'] for t in tv_shows_to_remove}
        to_remove_tv = [wl for wl in tv_in_watchlist if wl['id'] in tv_ids]
        if to_remove_tv:
            total = len(to_remove_tv)
            shows_removed = total
            print(f"Removing {total} TV shows from {username}'s watchlist...")
            for index, item in enumerate(to_remove_tv, 1):
                try:
                    account.removeFromWatchlist(item['item'])
                except BadRequest as e:
                    print(f"\n  ⚠️  Skipping: {item['item'].title} was already removed from {username}'s watchlist")
                print_progress(index, total, f"Removing TV shows from {username}'s watchlist")
            print()
    
    return movies_removed, shows_removed

def main():
    with open('config.yml') as f:
        config = yaml.safe_load(f)

    # Connect to Plex
    plex = PlexServer(config['plex_url'], config['plex_api_key'])
    admin_account = MyPlexAccount(token=config['plex_api_key'])
    
    # Initialize counters
    total_movies_removed = 0
    total_shows_removed = 0
    
    # Process users if specified in config
    if 'users' in config:
        # Parse the comma-separated list of users
        if isinstance(config['users'], str):
            # Split by comma and strip whitespace from each username
            users = [username.strip() for username in config['users'].split(',')]
        elif isinstance(config['users'], list):
            # If it's already a list, use it directly
            users = config['users']
        else:
            # Default to empty list if invalid format
            users = []
            print("⚠️  Invalid format for 'users' in config. Expected string or list.")
        
        # Get all users from the admin account
        try:
            all_plex_users = admin_account.users()
        except Exception as e:
            print(f"Error getting Plex users: {str(e)}")
            all_plex_users = []
        
        # Process each user specified in the config
        for username in users:
            print(f"\n{'='*50}")
            print(f"Processing {username}'s watchlist...")
            
            # Check if this is Admin
            if username == "Admin":
                print("Processing Admin account...")
                admin_movies, admin_shows = process_user_watchlist(admin_account, plex, config, "Admin")
                total_movies_removed += admin_movies
                total_shows_removed += admin_shows
                continue
            
            # Check if this is a home/managed user
            home_user = next((user for user in all_plex_users if user.home and user.title == username), None)
            
            try:
                # Check if we have credentials for this user
                if config.get('user_credentials', {}).get(username, {}):
                    user_credentials = config.get('user_credentials', {}).get(username, {})
                    if user_credentials.get('username') and user_credentials.get('password'):
                        try:
                            # Authenticate with provided credentials
                            user_account = MyPlexAccount(
                                username=user_credentials.get('username'),
                                password=user_credentials.get('password')
                            )
                            print(f"  Authenticated as {username} using credentials")
                            
                            # Process this user's watchlist
                            user_movies, user_shows = process_user_watchlist(
                                user_account, plex, config, username
                            )
                            
                            total_movies_removed += user_movies
                            total_shows_removed += user_shows
                        except Unauthorized:
                            print(f"  ⚠️  Authentication failed for {username}: Incorrect credentials")
                            print(f"  Skipping {username}")
                            continue
                        except Exception as e:
                            print(f"  ⚠️  Error authenticating {username}: {str(e)}")
                            print(f"  Skipping {username}")
                            continue
                    else:
                        print(f"  ⚠️  Incomplete credentials for {username}")
                        print(f"  Skipping {username}")
                        continue
                else:
                    print(f"  ⚠️  No credentials provided for {username}")
                    print(f"  Skipping {username}")
                    continue
                    
            except Exception as e:
                print(f"Error processing {username}: {str(e)}")
            print(f"{'='*50}")
    else:
        # If no users specified, just process Admin
        print("No users specified in config, processing Admin account only...")
        admin_movies, admin_shows = process_user_watchlist(admin_account, plex, config, "Admin")
        total_movies_removed += admin_movies
        total_shows_removed += admin_shows
    
    # Summary
    print("\nSummary:")
    print(f"Total movies removed from watchlists: {total_movies_removed}")
    print(f"Total TV shows removed from watchlists: {total_shows_removed}")

if __name__ == '__main__':
    main()
# 🎬 Plex Watchlist Cleaner 🧹

"Why are the movies and shows we watched still in our watch list? Can they not automatically be removed once we've watched them?"</br>
asked my spouse. Fair question.. Apparently Plex can only remove them if you watch them through Plex Movies or TV Shows. If you watch them through your own libraries they remain in watchlist.

This script automatically removes watched movies and/or TV shows from your Plex Watchlist.</br> 
Keep your watchlist clean and focused on content you haven't seen yet!

---

## ✨ Features
- **Finds and lists**: Retrieves your watchlist and lists movies and/or TV Shows you've already watched
- **Watchlist Cleanup**: Removes watched content from Plex Watchlist
- **Dry run**: `remove_from_watchlist` flag for dry-run or actual removal

---

## 🛠️ Installation

### 1️⃣ Download the Script
```sh
git clone https://github.com/netplexflix/Remove-from-Plex-Watchlist-when-watched.git
cd Remove-from-Plex-Watchlist-when-watched
```
![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Or simply download by pressing the green 'Code' button above and then 'Download Zip'.

### 2️⃣ Install Requirements
- Ensure you have [Python](https://www.python.org/downloads/) installed (`>=3.8` recommended)
- Open a Terminal in the script's directory
>[!TIP]
>Windows Users: <br/>
>Go to the script folder (where RFPW.py is).</br>
>Right mouse click on an empty space in the folder and click `Open in Windows Terminal`
- Install the required dependencies:
```sh
pip install -r requirements.txt
```
---

## ⚙️ Configuration

Rename `config.example.yml` to `config.yml` and update:

```yaml
# Required
plex_url: http://localhost:32400
plex_api_key: YOUR_PLEX_TOKEN
movie_library_name: "Movies"
tv_library_name: "TV Shows"

# Options
remove_from_watchlist: false  # Set true to enable removal
check_movies: true
check_tv_shows: true
```

**Configuration Guide:**  
- `plex_api_key`: [Find your Plex token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)  
- Libraries must match exact names in your Plex server  
- Set `remove_from_watchlist: false` for dry-run listing only  

---

## 🚀 Usage

Run the script with:
```sh
python RFPW.py
```

> [!TIP]
> Windows users can create a batch file for quick launching:
> ```batch
> "C:\Path\To\Python\python.exe" "Path\To\Script\RFPW.py"
> pause
> ```


**Sample Output:**
```
Fetching movie watchlist... [██████████] 100%
Scanning 1500 movies... [██████░░░░] 60%

Watched Movies in Watchlist:
- The Matrix (1999)
- Inception (2010)

Watched TV Shows in Watchlist:
- Breaking Bad (2008)

Removing 3 items from watchlist... [██████████] 100%
```


---

## ⚠️ Need Help or have Feedback?
- Join the [Discord](https://discord.gg/VBNUJd7tx3).
- [Open an Issue](https://github.com/yourusername/Remove-from-Plex-Watchlist-when-watched/issues)  

Like this project? Give it a ⭐!  

[![Buy Me A Coffee](https://img.shields.io/badge/Support-%F0%9F%8D%BA-yellow)](https://buymeacoffee.com/neekokeen)

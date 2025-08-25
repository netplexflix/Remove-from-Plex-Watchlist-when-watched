# 🎬 Plex Watchlist Cleaner 🧹

"Why are the movies and shows we watched still in our watch list? Can they not automatically be removed once we've watched them?"</br>
asked my spouse. Fair question.. Apparently Plex can only remove them if you watch them through Plex Movies or TV Shows. If you watch them through your own libraries they remain in watchlist.

This script automatically removes watched movies and/or TV shows from your Plex Watchlist.</br> 
Keep your watchlist clean and focused on content you haven't seen yet!

---

## ✨ Features
- 👥 **User Selection**: Manage watchlist for any user (requires login credentials)
- 🔎 **Finds and lists**: Retrieves your watchlist and lists movies and/or TV Shows you've already watched
- 🧹 **Watchlist Cleanup**: Removes watched content from Plex Watchlist
- ℹ️ **Dry run**: `remove_from_watchlist` flag for dry-run or actual removal

---

## 🛠️ Installation

### 1️⃣ Download the Script
```sh
git clone https://github.com/netplexflix/Remove-from-Plex-Watchlist-when-watched.git
cd Remove-from-Plex-Watchlist-when-watched
```
![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Or simply download by pressing the green 'Code' button above and then 'Download Zip'.

### 2️⃣ Install Requirements
- Ensure you have [Python](https://www.python.org/downloads/) installed (`>=3.11` recommended)
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

Rename `config.example.yml` to `config.yml` and update where necessary:

### Required
`plex_url:` http://localhost:32400 </br>
`plex_api_key:` [Where to find your plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) </br>
`movie_library_name:` e.g. "Movies" </br>
`tv_library_name:` e.g. "TV Shows" </br>

### Options
`remove_from_watchlist:` Set to `true` to enable removal. `false` for dry-run listing only  </br>
`check_movies:` whether or not to check movies </br>
`check_tv_shows:` whether or not to check TV Shows

### Users
> [!IMPORTANT]
> For any user other than Admin, you'll need to provide the login credentials to edit the watchlist.

`users:` Enter a comma separated list of users to process. You can enter `Admin` for the admin account.</br>
`user_credentials:` Enter the name, username and password for each user (except Admin) you'd like to process.

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

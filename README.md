# 🐧 Linux Command Cheat Sheet

Everything from today's workshop in one place. Keep it open during the recap mission. The mission instructions are at the [bottom](#-the-recap-mission).

> **Paths in 10 seconds**
> - `/` is the top of the filesystem. `~` is your home folder.
> - `.` is the current folder. `..` is the folder above it.
> - An **absolute** path starts with `/` (for example, `/home/alice/notes.txt`) and works from anywhere.
> - A **relative** path starts from where you are now (for example, `notes.txt` or `../notes.txt`).

---

## 1. Navigating Filesystems

| Command | What it does |
|---|---|
| `pwd` | Print the full path of the folder you're in |
| `ls` | List files and folders |
| `ls -l` | Long listing: permissions, owner, size, date |
| `ls -a` | Show **all** files, including hidden ones (names starting with `.`) |
| `ls -la` | Both at once. Probably the listing you'll use most |
| `ls -lh` | Sizes in human units (K, M, G) |
| `ls <folder>` | List another folder without going into it |
| `cd <folder>` | Go into a folder |
| `cd ..` | Go up one level |
| `cd ~` or `cd` | Go to your home folder |
| `cd -` | Go back to the folder you were just in |
| `cd /` | Go to the top of the filesystem |
| `tree` | Show folders and files as a tree (if it's installed) |

**Reading `ls -l`:** `-rwxr-xr-x` means: the first character is `-` for a file or `d` for a directory. After that come read/write/execute permissions for the owner, the group, and everyone else. An `x` means the file can be run.

## 2. Text Display

| Command | What it does |
|---|---|
| `cat <file>` | Print the whole file |
| `cat -n <file>` | Print it with line numbers |
| `head <file>` | First 10 lines |
| `head -n 5 <file>` | First 5 lines |
| `tail <file>` | Last 10 lines |
| `tail -n 5 <file>` | Last 5 lines |
| `tail -f <file>` | Keep printing new lines as they're added, e.g. a live log. Stop with `Ctrl+C` |
| `less <file>` | Scroll through a big file. Use the arrow keys or `Space`, `/word` to search, and `q` to quit |
| `echo "text"` | Print text |
| `echo $USER` / `echo $HOME` | Print a variable |
| `clear` | Clear the screen (or `Ctrl+L`) |

💡 Don't `cat` a file with thousands of lines. Use `head`, `tail`, `less` or `grep` instead.

## 3. File Management

| Command | What it does |
|---|---|
| `touch <file>` | Create an empty file, or update the timestamp of an existing one |
| `mkdir <folder>` | Create a folder |
| `mkdir -p a/b/c` | Create nested folders in one go |
| `cp <src> <dest>` | Copy a file (the original stays) |
| `cp -r <src> <dest>` | Copy a folder and everything in it |
| `mv <src> <dest>` | **Move** a file. The original is gone afterwards |
| `mv old.txt new.txt` | **Rename**: moving within the same folder |
| `mv dir/old.txt other/new.txt` | Move **and** rename in one command |
| `rm <file>` | Delete a file. ⚠️ There is no recycle bin |
| `rm -r <folder>` | Delete a folder and everything in it. ⚠️ Double-check first |
| `rmdir <folder>` | Delete an **empty** folder |
| `echo "text" > file` | Write text into a file. ⚠️ **Overwrites** what was there |
| `echo "text" >> file` | **Append** text to the end of a file |
| `command > file` | Save any command's output to a file, e.g. `ls -la > listing.txt` |

## 4. Searching

| Command | What it does |
|---|---|
| `grep word <file>` | Show lines containing `word`. Case-sensitive: `Error` ≠ `error` |
| `grep -i word <file>` | Ignore upper/lower case |
| `grep -n word <file>` | Also show line numbers |
| `grep -c word <file>` | Count the matching lines |
| `grep -v word <file>` | Show lines that **don't** match |
| `grep -r word <folder>` | Search every file in a folder |
| `wc <file>` | Count lines, words and characters |
| `wc -l <file>` | Count lines only |
| `wc -w <file>` | Count words only |
| `find . -name "*.txt"` | Find files by name under the current folder |

### Pipes `|`: chaining commands
A pipe sends one command's output into the next command:
```bash
ls | wc -l                    # how many files are here?
cat notes.txt | grep todo     # lines in notes.txt that contain "todo"
grep -i warn app.log | head -n 3   # the first 3 warnings
```

## 5. Running Scripts

| Command | What it does |
|---|---|
| `python3 script.py` | Run a Python script |
| `bash script.sh` | Run a shell script |
| `./script` | Run an executable script in the **current** folder. The `./` tells the shell where to look |
| `./script arg1 arg2` | Give the script values (arguments) |
| `./script 'a {tricky} value'` | Quote arguments that contain spaces or symbols |
| `chmod +x script` | Make a script executable, if you get "Permission denied" |

## Handy extras

| Command / key | What it does |
|---|---|
| `Tab` | Auto-complete file and folder names. Use it constantly! |
| `↑` / `↓` | Scroll through the commands you've typed before |
| `Ctrl+C` | Stop the running command |
| `history` | List your previous commands |
| `whoami` | Print your username |
| `man <command>` | The manual for a command (press `q` to quit) |
| `<command> --help` | A quick summary of a command's options |

---

## 🕵️ The Recap Mission

Your mission is to find **4 secret fragments** hidden in a set of folders and files, then combine them into a flag. **You are being timed.** The clock starts when you run the start script and stops when you submit the correct flag.

**Start** (if your instructor gives you a server address, run the `export` line first):
```bash
export MISSION_SERVER=http://<address-from-instructor>:8000
cd ~/linux-workshop-mission      # the folder you cloned, where start_mission.py is
python3 start_mission.py
```
This creates a **different** folder, `~/linux_mission` (with an underscore). That's where the mission happens: go in there and read the README.

**Submit** (from `~/linux_mission`, keeping the single quotes):
```bash
./submit.py 'FLAG{fragment1-fragment2-fragment3-fragment4}'
```

**Stuck?**
- Read every file the mission gives you. All the instructions are in there.
- Every script prints a hint when something's wrong. Read what it says!
- Broke something? Run `python3 start_mission.py` again (from `~/linux-workshop-mission`). It rebuilds your folder from the start, so you'll need to open the vault again. Your timer **doesn't** reset, and your flag stays the same.
- Don't delete `~/.linux_mission_token`. It proves to the server that you are you.
- Still stuck? Put your hand up.

Good luck, agent. 🐧

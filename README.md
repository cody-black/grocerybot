# grocerybot
The aim of grocerybot is to make ordering groceries online slightly less tedious by automatically adding items from a grocery list to your online cart.

---
## Setup
Grocerybot uses the Firefox browser. Get it here:
https://www.mozilla.org/firefox/browsers/

Also make sure that Python is installed or get it here:
https://www.python.org/downloads/
#### Linux
To use grocerybot on Linux, you can simply download the zip file from github or clone the repo using 
`git clone https://github.com/cody-black/grocerybot`.

To make sure you have the required packages installed, run 
`pip install -r requirements.txt`
in the grocerybot directory.

If you want to avoid having to log in every time you use grocerybot, you need to edit PROFILE_PATH in line 12 of grocerybot.py. Changing `PROFILE_PATH = "/home/username/.mozilla/firefox/whatever-your-profile-is"` to the proper path will tell the browser to use your Firefox profile instead of creating a temporary profile every time.
#### Other Operating Systems
Grocerybot hasn't been tested on other operating systems, but it will probably work. Follow the Linux instructions, except replace the geckodriver file with the one corresponding to your OS from https://github.com/mozilla/geckodriver/releases.

---

## Usage
In the grocerybot directory you should find list.txt, which is where you put your grocery list. The list.txt in this repo shows an example of how to do this:
> ground beef
> taco shells x2
> shredded cheese
> salsa
> tortilla chips

Each item should be on a separate line. How specific each item is is up to you. Adding `x#` (where `#` is a number) to the end of a line indicates that you want to add that many of that item to your cart. 

To use grocerybot, use the command `python3 grocerybot.py` (or `python grocerybot.py` depending on how your system is set up) in the grocerybot directory.

A Firefox browser window should open. Make sure you are logged in (see editing PROFILE_PATH above to stay logged in) and that you have selected the correct store. After that, press enter in the terminal window. From here, you can follow the instructions printed in the terminal.
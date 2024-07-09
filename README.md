# What is this?
Given a URL to a "read" Goodreads bookshelf, this script will download the book covers and create a collage. 

This was created out of personal desire to print and frame posters representing a year in reading. See [Examples](#examples) below.

# How do I use it?

### Requirements
* Python 3

### Steps

Go to your "read" bookshelf on Goodreads. Order by "Date read" descending. Copy the URL. It should look something like this:
```
https://www.goodreads.com/review/list/58160628-emily-books-with-emily-fox-on-youtube?order=d&per_page=100&shelf=read&sort=date_read&page=1
```

Remove the page # from the end, but leave the `page=`. If it's not at the end, move it there. It should look like this:
```
https://www.goodreads.com/review/list/58160628-emily-books-with-emily-fox-on-youtube?order=d&per_page=100&shelf=read&sort=date_read&page=
```

(Note: I had problems with the `utf8` URL parameter, so I removed it. You may have to escape characters in the query string depending on your shell.)

Feed this URL into the script:

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py -u <url>

e.g.

python3 main.py -u https://www.goodreads.com/review/list/58160628-emily-books-with-emily-fox-on-youtube\?order\=d\&per_page\=100\&shelf\=read\&sort\=date_read\&page\=
```

You can customize the output via the following optional parameters:

```
-d {date_read,date_added,none}, --date {date_read,date_added,none}
  Which date to use to limit how many books are shown. Default: date_read. Set to "none" to show all books

-a AGO, --ago AGO
  Number of days to collage backwards to, default 365

--min-width MIN_WIDTH
  Minimum width of collage. Default 6

--min-height MIN_HEIGHT
  Minimum height of collage. Default 6

-s, --swap-width-height
  Swaps preference from width to height, for rectangular layout algorithm. Enable if you want a wide image. Also use min-height.
```

# Notes

* The script might remove image(s) from the collage in order to make a rectangle
* The output is relatively high DPI. That can be adjusted here: `plt.savefig("collage.jpg", dpi=500, bbox_inches="tight", pad_inches=0)` 

# Examples

### Raw Output

![images/collage](https://github.com/gr-collage/blob/main/images/collage.jpg)

### Inspiration (with additional manual editing)
![frame](https://github.com/dmmatson/gr-collage/blob/main/frame.png?raw=true)

# Based On

https://joshualoong.com/2019/02/05/Programmatically-Creating-a-500-Book-Cover-Collage/

# Disclaimer

This project is not affiliated with Goodreads or Amazon.

I have no idea if this is against Goodreads' terms of service. Use at your own risk.

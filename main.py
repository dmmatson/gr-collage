import argparse
import cv2
import glob
import matplotlib.pyplot as plt
import numpy as np
import random
import requests
import sys

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from natsort import natsorted


def user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
    ]
    return random.choice(agents)


def find_largest_factors(even_number):
    sqrt_num = int(even_number**0.5)

    factor1 = 0
    factor2 = 0

    for i in range(sqrt_num, 1, -1):
        if even_number % i == 0:
            factor1 = i
            factor2 = even_number // i
            break

    return factor1, factor2


parser = argparse.ArgumentParser()
parser.add_argument(
    "-u",
    "--url",
    help="URL to read shelf, with page= at the end",
    required=True
)
parser.add_argument(
    "-d",
    "--date",
    choices=["date_read", "date_added", "none"],
    default="date_read",
    help='Which date to use to limit how many books are shown. Default: date_read. Set to "none" to show all books'
)

args = parser.parse_args()

# Get read book cover URLs
page = 0
covers = []
done = False

while not done:
    page += 1

    url = args.url + str(page)    
    headers = {"User-Agent": user_agent()}
    print(f"Getting page {url}")
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"id": "books"})
    books = table.find_all("tr", {"class": "bookalike review"})
    if len(books) == 0:
        print("reached final page!")
        done = True

    for book in books:
        cover_url = (
            book.find("img")["src"]
            .replace("SY75", "")
            .replace("SX50", "")
            .replace("__", "")
            .replace("..", ".")
            .replace("._.", ".")
        )
        title = book.find("td", {"class": "field title"}).text.replace("\n", "").strip()

        if args.date != "none":
            date = (
                book.find("td", {"class": args.date})
                .text.replace("date read", "")
                .replace("not set", "")
            )
            date = list(filter(None, date.split("\n")))
            if len(date) > 0:
                date = date[0]
                if len(date.replace(",", " ").split(" ")) < 3:
                    month, year = date.replace(",", " ").split(" ")
                    date = f"{month} 1, {year}"
                date = datetime.strptime(date, "%b %d, %Y")
                if date < datetime.now() - timedelta(days=1 * args.ago):
                    done = True
                    break

        if "nophoto" in cover_url:
            continue

        print(title, date, cover_url)
        covers.append(cover_url)

# Download covers
print("\n")
for i, cover in enumerate(covers):
    print(f"Download progress: {round((float(i) / len(covers)) * 100)}%")
    image = requests.get(cover).content
    with open(f"image{i}.jpg", "wb") as handler:
        handler.write(image)


# Adjust number of images so we have a rectangle
print("\n")
image_paths = glob.glob("image*.jpg")
image_paths = natsorted(image_paths)
num_imgs = len(image_paths)
width, height = find_largest_factors(num_imgs)
while width < 6:
    print(f"Adjust for rectangle, pruning {image_paths.pop()}")
    num_imgs = len(image_paths)
    width, height = find_largest_factors(num_imgs)

# Create collage
print("\n")
print(f"Creating collage from {num_imgs} images")
column_count = 1
column_list = []
column_matrix = []

for path in image_paths:
    img = cv2.imread(path, 1)
    img = cv2.resize(img, (200, 300))

    if column_count < height:
        column_list.append(img)
        column_count += 1
    elif column_count == height:
        column_list.append(img)
        column = np.vstack(column_list)
        column_matrix.append(column)
        column_count = 1
        column_list = []

if len(column_list) > 0:
    column = np.vstack(column_list)
    column_matrix.append(column)

collage = np.hstack(column_matrix)
plt.figure(figsize=(60, 30))
plt.axis("off")
plt.imshow(collage[:, :, ::-1])
plt.savefig("collage.jpg", dpi=500, bbox_inches="tight", pad_inches=0)
plt.close()

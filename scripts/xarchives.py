#!/usr/bin/env python3
from datetime import datetime
import json
import locale
import re

prelude = """
<!--
    Copyright (c) 2025 antiochus wilson
    Content licensed under Creative Commons Attribution-NonCommercial 4.0 International License
    https://creativecommons.org/licenses/by-nc/4.0/
-->
<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>xarchives</title>
        <link rel="stylesheet" href="./assets/styles.css" />
        <script src="./assets/tlsearch.js" defer></script>
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="index.html">home</a></li>
                    <li><a href="xarchives.html">xarchives</a></li>
                    <li><a href="journal.html">journal</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h1>xarchives</h1>
            <section id="search">
                <input
                    type="text"
                    id="search-bar"
                    placeholder="Search xarchives..."
                />
            </section>
            <section id="timeline">
                <ul id="entries">
"""
print(prelude)
with open('../data/cleanedtweets.json') as f:
    d = json.load(f)
    locale.setlocale(locale.LC_ALL, '')
    url_pattern = r'https?://[^\s]+'
    for e in d:
        li = ""
        dt = datetime.strptime(e['timestamp'], "%a %b %d %H:%M:%S %z %Y")
        fdt = dt.strftime("%c")
        if "https://t.co" in e['content']:
            continue
        if "twitter.com/antiochuswilson/status" in e['content']:
            urls = re.findall(url_pattern, e['content'])
            found_index = 0
            for url in urls:
                if "antiochuswilson" in url:
                    e['content'] = re.sub(re.escape(url), '', e['content'])
                    break
                found_index += 1
            qt_id = urls[found_index].split('/')[-1]
            qt = [j for j in d if j['id'] == qt_id]
            if len(qt) == 0:
                continue
            qt = qt[0]
            qdt = datetime.strptime(qt['timestamp'], "%a %b %d %H:%M:%S %z %Y")
            qfdt = qdt.strftime("%c")
            li = f"""
                        <li id="{e['id']}" class="entry">
                            <span class="timestamp">{fdt}</span>
                            <p class="content">{e['content']}</p>
                            <div id="q{qt['id']}" class="qt">
                                <span class="timestamp>{qfdt}</span>
                                <p> class="content>{qt['content']}</p>
                            </div>
                        </li>
            """
        else:    
            dt = datetime.strptime(e['timestamp'], "%a %b %d %H:%M:%S %z %Y")
            fdt = dt.strftime("%c")
            li = f"""
                        <li id="{e['id']}" class="entry">
                            <span class="timestamp">{fdt}</span>
                            <p class="content">{e['content']}</p>
                        </li>
            """
        print(li)

postscript = """
                </ul>
            </section>
        </main>
        <footer>
            <p>&copy; 2025</p> |
            <a href="./assets/license.txt">Content License</a> |
            <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>
        </footer>
    </body>
</html>
"""
print(postscript)

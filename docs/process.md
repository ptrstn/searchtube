# YouTube Search Reverse Engineering Process

## Prerequisites

1. Open Incognito Chrome Browser
2. Browse to youtube.com
3. Press ```CTRL+SHIFT+I```
4. Switch to Network

## Search Suggestion

1. Type text in YouTube search bar
2. Switch to DevTools (```CTRL+SHIFT+I```) 
3. Look for ```search?client=youtube[...]``` request
4. Right click -> Copy -> Copy as cURL
5. Paste in file ```request.txt```
6. Test out command in console
7. pip install [uncurl](https://pypi.org/project/uncurl/)
8. install [xclip](https://archlinux.org/packages/extra/x86_64/xclip/)
9. paste command (dont enter):

```bash
xclip -selection clipboard -o | tr '\\\r\n' ' ' | tr -s " " | sed 's/"/\"/g' | uncurl > request.py
```

10. copy contents of ```request.txt```
11. execute command
12. play with ```request.py```

import webbrowser, subprocess
async def openurl(ctx,*,url:str):
 if not url.startswith(('http://','https://')):url='https://'+url
 webbrowser.open(url)
 await ctx.send(f"URL opened at: {url}")
async def search(ctx, *, query: str):
    search_url = f"https://www.bing.com/search?q={query}"
    try:
        default_browser = webbrowser.get()
        if default_browser is None: subprocess.Popen(['start', 'msedge', search_url], shell=True)
        else: webbrowser.open(search_url)
    except webbrowser.Error: subprocess.Popen(['start', 'msedge', search_url], shell=True)
    await ctx.send(f"Opened URL: {search_url}")
#now imagine using this in front of people
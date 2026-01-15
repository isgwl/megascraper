from seleniumbase import SB

def fb_marketplace_search_results(sb: SB, url):
    sb.cdp.get(url)
    sb.cdp.scroll_down(amount=25)
    
    #get all item links eg: /marketplace/item/*
    item_links = []
    for el in sb.cdp.select_all("*"):
        link = el.get_attribute("href")
        if "/marketplace/item/" in link:
            item_links.append(link[0:link.find("?")])
    
    return {
        "url": url,
        "data":None,
        "new_links": item_links
    }
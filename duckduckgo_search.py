from duckduckgo_search import DDGS

def search_duckduckgo(query, max_results=5):
    """
    يقوم بالبحث في DuckDuckGo وإرجاع النتائج كقائمة من القواميس.
    """
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "href": r.get("href", ""),
                "body": r.get("body", "")
            })
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        results = search_duckduckgo(query)
        for r in results:
            print(f"Title: {r['title']}\nURL: {r['href']}\nBody: {r['body']}\n{'-'*20}")
    else:
        print("Usage: python3 duckduckgo_search.py <query>")

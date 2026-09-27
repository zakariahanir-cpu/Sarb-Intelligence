from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class _ResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self._current = None
        self._capture = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "result__a" in attrs.get("class", ""):
            self._current = {"title": "", "href": attrs.get("href", ""), "body": ""}
            self._capture = True
        elif tag in {"a", "div"} and self._current and "result__snippet" in attrs.get("class", ""):
            self._capture = True

    def handle_data(self, data):
        if self._capture and self._current:
            self._current["title" if not self._current["title"] else "body"] += data.strip()

    def handle_endtag(self, tag):
        if tag == "a" and self._current:
            self.results.append(self._current)
            self._current = None
            self._capture = False


def search_duckduckgo(query, max_results=5):
    """Search DuckDuckGo without importing a same-named local module."""
    request = Request(
        "https://html.duckduckgo.com/html/?" + urlencode({"q": query}),
        headers={"User-Agent": "Sarb-Intelligence/1.0"},
    )
    try:
        with urlopen(request, timeout=10) as response:
            parser = _ResultParser()
            parser.feed(response.read().decode("utf-8", errors="replace"))
            return parser.results[:max_results]
    except Exception as exc:
        return [{"title": "Search unavailable", "href": "", "body": str(exc)}]

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        results = search_duckduckgo(query)
        for r in results:
            print(f"Title: {r['title']}\nURL: {r['href']}\nBody: {r['body']}\n{'-'*20}")
    else:
        print("Usage: python3 duckduckgo_search.py <query>")

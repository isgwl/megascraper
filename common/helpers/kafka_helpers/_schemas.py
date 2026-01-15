import json
from importlib.resources import files

_base = files(__package__).joinpath("schemas")

targetPageSchema = json.loads((_base / "target_page.json").read_text(encoding="utf-8"))
scrapeResultSchema = json.loads((_base / "scrape_result.json").read_text(encoding="utf-8"))

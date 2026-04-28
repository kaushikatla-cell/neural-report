# Neural Report — local checks (requires Python 3 + Pillow for og)
.PHONY: feeds sync og check quality publish-check

feeds:
	python3 scripts/generate_feeds.py

sync:
	python3 scripts/sync_site_pages.py

og:
	python3 scripts/generate_og_images.py

check:
	python3 scripts/check_docs.py

quality:
	python3 scripts/check_briefs.py

publish-check:
	bash scripts/publish-check.sh

# Neural Report — local checks (requires Python 3 + Pillow for og)
.PHONY: feeds og check publish-check

feeds:
	python3 scripts/generate_feeds.py

og:
	python3 scripts/generate_og_images.py

check:
	python3 scripts/check_docs.py

publish-check:
	bash scripts/publish-check.sh

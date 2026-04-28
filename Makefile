# Neural Report — local checks (requires Python 3)
.PHONY: feeds check publish-check

feeds:
	python3 scripts/generate_feeds.py

check:
	python3 scripts/check_docs.py

publish-check:
	bash scripts/publish-check.sh

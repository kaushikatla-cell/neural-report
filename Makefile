# Neural Report — local checks (requires Python 3 + Pillow for og)
.PHONY: manifest feeds sync dashboard library search-index transparency og check quality snapshot-links bootstrap publish-check

manifest:
	python3 scripts/check_manifest.py

feeds:
	python3 scripts/generate_feeds.py

sync:
	python3 scripts/sync_site_pages.py

dashboard:
	python3 scripts/generate_dashboard.py

library:
	python3 scripts/generate_library_page.py

search-index:
	python3 scripts/generate_search_index.py

transparency:
	python3 scripts/generate_transparency_page.py

og:
	python3 scripts/generate_og_images.py

check:
	python3 scripts/check_docs.py

quality:
	python3 scripts/check_briefs.py

snapshot-links:
	python3 scripts/snapshot_external_links.py

bootstrap:
	@echo "Usage:"
	@echo "  python3 scripts/bootstrap_brief.py --date YYYY-MM-DD --slug topic --title \"...\" --summary \"...\" --tags \"a,b,c\" --run-all"

publish-check:
	bash scripts/publish-check.sh

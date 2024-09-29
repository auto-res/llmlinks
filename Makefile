.PHONY: bump_version build publish

bump_version:
	uv run bumpversion patch

build:
	uv build

publish:
	uvx twine upload dist/* 

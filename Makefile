.PHONY: build release test clean

test:
	@tox

quicktest:
	@tox -q -e py39

build:
	@python -m build

release:
	@twine upload --skip-existing --verbose dist/*

clean:
	@rm -rf build/*
	@find . -name __pycache__ | xargs rm -rf

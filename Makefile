.PHONY: build release test clean

test:
	rm -rf build
	py.test --cov=nexusmaker
	coverage html

build:
	python setup.py sdist bdist_wheel

release:
	python setup.py sdist bdist_wheel upload

clean:
	rm -rf build/*
	find . -name __pycache__ | xargs rm -rf

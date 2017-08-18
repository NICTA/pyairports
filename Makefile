build: clean test clean source_dist

clean:
	rm -rf build/ dist/ *.egg-info nosetests.xml pylint.out
	find . -name "*.pyc" -delete

clobber: clean
	rm -rf .pyenv

test:
	nosetests -v .

dist: source_dist build_dist

source_dist:
	python setup.py sdist

build_dist:
	python setup.py bdist_wheel

virtualenv:
	test -d .pyenv || virtualenv .pyenv
	./.pyenv/bin/pip install pip --upgrade

environment: clobber virtualenv

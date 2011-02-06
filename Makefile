.PHONY: clean-pyc test

all: clean-pyc test

test: clean-pyc
	#python test_noextref.py -v
	python setup.py test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

doc:
	python setup.py build_sphinx

pypi: test doc
	python setup.py sdist upload
	python setup.py upload_docs --upload-dir=build/sphinx/html

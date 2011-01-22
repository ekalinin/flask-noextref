.PHONY: clean-pyc test

all: clean-pyc test

test: clean-pyc
	#python test_noextref.py -v
	python setup.py test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

doc:
	#$(MAKE) -C docs html
	python setup.py build_sphinx

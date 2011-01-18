.PHONY: clean-pyc test

all: clean-pyc test

test:
	python test_noextref.py -v

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

doc:
	python setup.py build_sphinx
	#$(MAKE) -C docs html

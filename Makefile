COMNETSEMU = comnetsemu/*.py
TEST = comnetsemu/test/*.py
EXAMPLES = examples/*.py
PYTHON ?= python3
PYSRC = $(COMNETSEMU) $(EXAMPLES)
P8IGN = E251,E201,E302,E202,E126,E127,E203,E226
PREFIX ?= /usr
DOCDIRS = doc/html doc/latex

CFLAGS += -Wall -Wextra

all: codecheck

clean:
	rm -rf build dist *.egg-info *.pyc $(DOCDIRS)

codecheck: $(PYSRC)
	@echo "*** Running code check"
	pyflakes $(PYSRC)
	pylint --rcfile=.pylint $(PYSRC)
	pep8 --repeat --ignore=$(P8IGN) `ls $(PYSRC)`

errcheck: $(PYSRC)
	@echo "*** Running check for errors only"
	pyflakes $(PYSRC)
	pylint -E --rcfile=.pylint $(PYSRC)

test_examples: $(COMNETSEMU)
	@echo "*** Running functional examples of the emulator"
	$(PYTHON) ./examples/dockerhost.py
	$(PYTHON) ./examples/dockerindocker.py

check_installer: ./util/install.sh
	@ echo "*** Check installer"
	bash ./check_installer.sh


install:
	$(PYTHON) setup.py install

develop: $(MNEXEC) $(MANPAGES)
	$(PYTHON) setup.py develop

.PHONY: doc

doc: $(PYSRC)
	doxygen doc/doxygen.cfg
	make -C doc/latex

include common.mk

ifdef PIP_INDEX_URL
	PIP_INSTALL := $(BIN)/pip install -i $(PIP_INDEX_URL) -q
else
	PIP_INSTALL := $(BIN)/pip install -q
endif

SOURCES := server tests
STYLE_CMD := find $(SOURCES) -name '*.py' -exec $(BIN)/flake8 {} +

TEST_OPTS += --with-xunit

$(BIN)/python:
	@printf "$(BOLD)Creating virtualenv...$(NORMAL)\n"
	virtualenv $(DEVELOP)

$(BIN)/nosetests: $(BIN)/python
	$(PIP_INSTALL) nose

$(BIN)/flake8: $(BIN)/python
	$(PIP_INSTALL) flake8

.PHONY: develop
develop: $(BIN)/python
	$(PIP_INSTALL) -e .[test]

.PHONY: clean
clean:
	@printf "$(BOLD)Removing virtualenv...$(NORMAL)\n"
	rm -rf $(DEVELOP)
	rm -rf server.egg-info nosetests.xml

.PHONY: test
test: develop $(BIN)/nosetests
	. $(DEVELOP)/bin/activate; $(BIN)/nosetests $(TEST_OPTS) tests

.PHONY: style
style: develop $(BIN)/flake8
	$(STYLE_CMD)

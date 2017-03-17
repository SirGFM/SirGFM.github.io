
# Setup the path to mistune lib (if not on the system's)
MISTUNE_PATH ?= /opt/mistune
ifneq (, $(MISTUNE_PATH))
    PPATH := PYTHONPATH=$(PYTHONPATH):$(MISTUNE_PATH)
endif

SRC := $(wildcard src/*.md)
OBJ := $(SRC:src/%.md=%.html)

.PHONE: all clean start README.html

all: start clean_nav $(OBJ)
	@ echo -n "Finished rendering: "
	@ date

%.html: src/%.md
	@ echo "Rendering $@..."
	$(PPATH) python src/generator/md_renderer.py $(PWD)/$< $(PWD)/$@ $(PWD)/src/nav.txt

start:
	@ echo -n "Starting rendering of site... "
	@ date

# Force everything to be rebuilt
clean_nav: src/nav.txt
	@ echo "Sidebar was modified! Recreating everything..."
	@ rm -f $(OBJ)
	@ touch clean_nav

clean:
	@ echo "Cleaning all files..."
	@ rm -f $(OBJ)

# Ignore README.html
README.html:
	@ # Do nothing...


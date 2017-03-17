
# Add the generator to the python path
PYTHONPATH := $(PYTHONPATH):$(PWD)/src/generator/
# Setup the path to mistune lib (if not on the system's)
MISTUNE_PATH ?= /opt/mistune
ifneq (, $(MISTUNE_PATH))
    PPATH := PYTHONPATH=$(PYTHONPATH):$(MISTUNE_PATH)
endif

SRC := $(wildcard src/*.md)
OBJ := $(SRC:src/%.md=%.html)

.SUFFIXES:
.PHONY: all clean start README.html

all: start clean_nav $(OBJ)
	@ echo -n "Finished rendering: "
	@ date

start:
	@ echo -n "Starting rendering of site... "
	@ date

%.html: src/%.md
	@ echo "Rendering $@..."
	$(PPATH) python src/generator/md_renderer.py $(PWD)/$< $(PWD)/$@ $(PWD)/src/nav.txt

# Include every rule from a depency (properly tracks header dependency)
-include $(OBJ:%.html=%.d)

# Creates the dependency list
%.d: src/%.md
	@ echo 'Creating dependency list for $<...'
	@ python src/generator/dependency_tracker.py $< $@ > $@

# Force everything to be rebuilt
clean_nav: src/nav.txt
	@ echo "Sidebar was modified! Recreating everything..."
	@ rm -f $(OBJ) $(OBJ:%.html=%.d)
	@ touch clean_nav

clean:
	@ echo "Cleaning all files..."
	@ rm -f $(OBJ) $(OBJ:%.html=%.d)

# Ignore README.html
README.html: src/README.md
	@ # Do nothing...


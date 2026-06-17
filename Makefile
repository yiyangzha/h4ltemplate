CXX ?= c++
CXXFLAGS ?= -O3 -DNDEBUG -Wall -Wextra -Wpedantic
ROOTCFLAGS := $(shell root-config --cflags)
ROOTLIBS := $(shell root-config --libs)

all: modify_nanoaod

modify_nanoaod: modify_nanoaod.cpp
	$(CXX) $(CXXFLAGS) $(ROOTCFLAGS) -o $@ $< $(ROOTLIBS)

.PHONY: all

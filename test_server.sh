#!/bin/bash

venv/bin/python generator.py
venv/bin/python -m http.server --directory ./docs/

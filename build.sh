#!/bin/bash

poetry install
poetry run pyinstaller desktop_overlay.spec

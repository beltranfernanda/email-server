#!/bin/bash

coverage run -m unittest discover
coverage report --fail-under 90

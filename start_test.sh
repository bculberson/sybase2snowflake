#!/bin/bash

./wait-for.sh dksybase:5000 -- python ./test_dataset.py
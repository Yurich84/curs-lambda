#!/bin/bash

rm -f code.zip;
zip code.zip *.py;
aws lambda update-function-code --function-name curs --zip-file fileb://code.zip;
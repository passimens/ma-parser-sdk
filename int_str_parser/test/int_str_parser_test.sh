#!/bin/bash

src_files=`ls data/*.txt`
for eachfile in $src_files
do
  cat $eachfile | PARSER_SRC_FILE=$eachfile PYTHONPATH={$PYTHONPATH}:`pwd`/../..:`pwd`/../../parser_api:`pwd`/../../magritte/Magritte python3 -m unittest int_str_parser_test.TestIntStrParser
done

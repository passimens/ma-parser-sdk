#!/bin/bash

src_files=`ls data/*.txt`
for eachfile in $src_files
do
  cat $eachfile | PARSER_SRC_FILE=$eachfile PYTHONPATH={$PYTHONPATH}:`pwd`/..:`pwd`/../parser_api python3 -m unittest any_parser_test.TestAnyParser
done

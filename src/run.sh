#!/usr/bin/env bash

cd documents/processing/QuestionGeneration/
cat $1 | sh run.sh > $2
cd ../../../
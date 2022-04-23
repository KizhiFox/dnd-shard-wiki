#!/bin/bash

function ctrl_c() {
    kill $serv_pid
    exit
}

trap ctrl_c INT

./venv/bin/python -m http.server --directory ./docs/ &
serv_pid=$!

while true
do
    ./venv/bin/python ./generator.py
    inotifywait ./markdown/ ./favicon.ico ./style.css -r -e modify -e create -e delete -e move
done


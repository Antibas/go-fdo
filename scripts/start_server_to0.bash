#!/bin/bash

usage(){
    echo "Starts the server with TO1 IP and optionally gets a GUID"
    echo "Usage: ./start_server.bash [-r] [-c]"
    echo "-r: Restart"
    echo "-c: Clean up docker system"
    exit 1
}

while getopts ":hrcg:" opt; do
    case ${opt} in
        h)
            usage
            ;;
        r)
            sudo docker-compose -f server-to0-docker-compose.yaml down
            ;;
        c)
            sudo docker system prune -f
            ;;
        ?)
            echo "Invalid option: -${OPTARG}."
            usage
            ;;
    esac
done
# sudo docker-compose -f server-to0-docker-compose.yaml up --build -d
go run ./examples/cmd server -http 127.0.0.1:9997 -to0 http://127.0.0.1:9997 -db ./test.db
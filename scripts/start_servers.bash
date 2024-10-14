#!/bin/bash

usage(){
    echo "Starts the servers"
    echo "Usage: ./start_server.bash [-c]"
    echo "-c: Clean up docker system"
    exit 1
}

while getopts ":hc" opt; do
    case ${opt} in
        h)
            usage
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
# sudo docker-compose up --build -d
go run ./examples/cmd server -http 127.0.0.1:9999 -db ./test.db
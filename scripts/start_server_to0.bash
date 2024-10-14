#!/bin/bash

usage(){
    echo "Starts the server with TO1 IP and optionally gets a GUID"
    echo "Usage: ./start_server.bash [-r] [-c] [-g GUID]"
    echo "-r: Restart"
    echo "-c: Clean up docker system"
    echo "-g GUID: The GUID from the client"
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
        g)
            # echo "GUID=${OPTARG}" > guid.env
            # sudo docker-compose -f server-to0-guid-docker-compose.yaml  --env-file guid.env up --build -d
            exit 0;
            ;;
        ?)
            echo "Invalid option: -${OPTARG}."
            usage
            ;;
    esac
done
# sudo docker-compose -f server-to0-docker-compose.yaml up --build -d
go run ./examples/cmd server -http 127.0.0.1:9997 -to0 http://127.0.0.1:9999 -db ./test.db
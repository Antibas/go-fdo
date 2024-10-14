#!/bin/bash

usage(){
    echo "Stops the system"
    echo "Usage: ./start_system.bash [-c]"
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
sudo docker-compose -f docker-compose.yaml -f server-to0-guid-docker-compose.yaml down
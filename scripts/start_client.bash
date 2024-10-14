#!/bin/bash

# usage(){
#     echo "Initializes & starts the client"
#     echo "Usage: ./start_client.bash [-c]"
#     echo "-c: Clean up docker system"
#     exit 1
# }

# while getopts ":hc" opt; do
#     case ${opt} in
#         h)
#             usage
#             ;;
#         c)
#             sudo docker system prune -f
#             ;;
#         ?)
#             echo "Invalid option: -${OPTARG}."
#             usage
#             ;;
#     esac
# done
go run ./examples/cmd client -di http://127.0.0.1:9999
go run ./examples/cmd client
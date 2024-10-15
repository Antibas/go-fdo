go run ./examples/cmd client -di http://127.0.0.1:9997
go run ./examples/cmd client -print | grep GUID | awk '{print $2}'
go run ./examples/cmd server -http 127.0.0.1:9997 -to0 http://127.0.0.1:9997 -to0-guid $1 -db ./test.db
go run ./examples/cmd client -rv-only
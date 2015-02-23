package main

// Need versioning as the server needs to

type Service interface {
	echo(message string) string
}

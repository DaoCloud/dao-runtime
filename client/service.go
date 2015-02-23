package main

// Need versioning as the server needs to

type Service interface {
	Echo(message string) (string, error)
}

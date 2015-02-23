package main

type service struct {
}

func (s service) echo(message string) string {
	return message
}

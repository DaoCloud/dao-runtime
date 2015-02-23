// Copyright DaoCloud Inc. All rights reserved.
package main

import (
	"errors"
)

var s service

func run_command(command Command) (string, error) {
	if command.Name == "echo" {
		return s.Echo(command.Message)
	} else {
		return "", errors.New("Unrecognized command")
	}
}

// Copyright DaoCloud Inc. All rights reserved.
package main

type service struct {
}

func (s service) Echo(message string) (string, error) {
	return message, nil
}

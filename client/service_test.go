// Copyright DaoCloud Inc. All rights reserved.
package main

import (
	"testing"
)

func TestEcho(t *testing.T) {
	messages := []string{
		"hello, world",
	}

	s := &service{}
	for _, message := range messages {
		received, err := s.Echo(message)
		if received != message {
			t.Errorf("Echo(%q) == %q, want %q", message, received, message)
		}
		if err != nil {
			t.Errorf("Echo() returned nil")
		}
	}
}

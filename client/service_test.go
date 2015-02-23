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
		received := s.echo(message)
		if received != message {
			t.Errorf("Echo(%q) == %q, want %q", message, received, message)
		}
	}
}

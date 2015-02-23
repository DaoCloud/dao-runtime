package main

import (
	"flag"
	"fmt"
	"os"
	"os/signal"
	"path"
	"syscall"
	"time"
)

func usage() {
	fmt.Fprintf(os.Stderr, "Usage %s [flags]\n", path.Base(os.Args[0]))
	flag.PrintDefaults()
	os.Exit(1)
}

func cleanup() {
	Unregister()
	fmt.Println(runtimeName + " unregistered")
}

func exit(status int) {
	cleanup()
	os.Exit(status)
}

var runtimeServer string
var runtimeName string

func main() {
	flag.StringVar(&runtimeServer, "server", "localhost:5000", "server address")
	flag.StringVar(&runtimeName, "name", "", "runtime name")

	flag.Parse()

	if runtimeName == "" {
		fmt.Fprintln(os.Stderr, "Error: name cannot be empty\n")
		usage()
	}

	// Signal handler
	c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGINT)
	signal.Notify(c, syscall.SIGTERM)
	go func() {
		<-c
		cleanup()
		os.Exit(0)
	}()

	// Register runtime
	Register()
	fmt.Println(runtimeName + " registered")

	// Get remote commands from server every 2 seconds
	ticker := time.NewTicker(2 * time.Second)
	go func() {
		for {
			select {
			case <-ticker.C:
				commands := Polling()
				for _, command := range commands {
					fmt.Println(command)
				}
			}
		}
	}()

	quit := make(chan struct{})
	<-quit
}

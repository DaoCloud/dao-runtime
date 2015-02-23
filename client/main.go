// Copyright DaoCloud Inc. All rights reserved.
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
		exit(0)
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
					// Process in parallel
					go func(command Command) {
						result, err := run_command(command)
						fmt.Printf("command of %d: %s, %s\n", command.SeqId, command.Name, command.Message)
						CallbackResult(command, result, err)
						if err != nil {
							fmt.Fprintf(os.Stdout, "result of %d: %q\n", command.SeqId, err)
						} else {
							fmt.Fprintf(os.Stdout, "result of %d: %q\n", command.SeqId, result)
						}
					}(command)
				}
			}
		}
	}()

	// Blocks main
	quit := make(chan struct{})
	<-quit
}

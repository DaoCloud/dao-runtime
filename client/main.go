package main

import (
	"flag"
	"fmt"
	"os"
	"path"
)

func usage() {
	fmt.Fprintf(os.Stderr, "Usage %s [flags]\n", path.Base(os.Args[0]))
	flag.PrintDefaults()
	os.Exit(1)
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

	Register()
	fmt.Println(runtimeName + " registered")
	defer func() {
		Unregister()
		fmt.Println(runtimeName + " unregistered")
	}()
}

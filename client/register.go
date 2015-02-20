package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"
)

// Extremely pessimistic error handling. Anything went wrong, commit a suicide.
// Demonstration purpose only.

func Register() {
	service := &Service{
		Name: runtimeName,
	}

	body, err := json.Marshal(service)
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		os.Exit(1)
	}

	registerUrl := &url.URL{
		Scheme: "http",
		Host:   runtimeServer,
		Path:   "/api/v1/runtimes",
	}
	resp, err := http.Post(registerUrl.String(), "application/json", bytes.NewReader(body))
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		os.Exit(1)
	}

	if resp.StatusCode != 200 {
		fmt.Fprintf(os.Stderr, "Error: register failed with %s", resp.Status)
		os.Exit(1)
	}
}

func Unregister() {
	unregisterUrl := &url.URL{
		Scheme: "http",
		Host:   runtimeServer,
		Path:   "/api/v1/runtimes/" + runtimeName,
	}
	req, err := http.NewRequest("DELETE", unregisterUrl.String(), nil)
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		os.Exit(1)
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		os.Exit(1)
	}

	if resp.StatusCode != 200 {
		fmt.Fprintf(os.Stderr, "Error: unregister failed with %s", resp.Status)
		os.Exit(1)
	}
}

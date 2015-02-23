// Copyright DaoCloud Inc. All rights reserved.
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
)

func Polling() []Command {
	pollingUrl := &url.URL{
		Scheme: "http",
		Host:   runtimeServer,
		Path:   fmt.Sprintf("/api/v1/runtimes/%s/requests", runtimeName),
	}

	resp, err := http.Get(pollingUrl.String())
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		exit(1)
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)

	commands := make([]Command, 5)
	err = json.Unmarshal(body, &commands)
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		exit(1)
	}

	return commands
}

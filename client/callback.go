package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"
)

func CallbackResult(command Command, result string, err error) {
	callbackUrl := &url.URL{
		Scheme: "http",
		Host:   runtimeServer,
		Path:   fmt.Sprintf("/api/v1/runtimes/%s/callback", runtimeName),
	}

	callbackResult := &Callback{
		OK:     err == nil,
		Result: result,
		SeqId:  command.SeqId,
	}

	body, err := json.Marshal(callbackResult)
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		exit(1)
	}

	resp, err := http.Post(callbackUrl.String(), "application/json", bytes.NewReader(body))
	if err != nil {
		fmt.Fprintln(os.Stderr, err.Error())
		exit(1)
	}

	if resp.StatusCode != 200 {
		fmt.Fprintf(os.Stderr, "Error: callback failed with %s", resp.Status)
		exit(1)
	}
}

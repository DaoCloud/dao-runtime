package main

type Runtime struct {
	Name string `json:"name"`
}

type Command struct {
	Name    string `json:"name"`
	SeqId   int    `json:"seq_id"`
	Message string `json:"message"`
}

type Callback struct {
	OK     bool   `json:"ok"`
	SeqId  int    `json:"seq_id"`
	Result string `json:"result"`
}

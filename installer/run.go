package main

import (
	"fmt"
	"os/exec"
)

func main() {
	cmd := exec.Command("/osu-python/venv/Scripts/python.exe", "-m", "osu_python")
	cmd.Dir = "/osu-python/source"
	err := cmd.Run()
	if err != nil {
		fmt.Printf("Error occurred: %s. Please report this issue to developers https://github.com/JustLian/osu-python", err)
	}
}

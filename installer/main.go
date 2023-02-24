package main

import (
	"archive/zip"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

func unzip(src, dest string) error {
	// https://stackoverflow.com/a/24430720/16778733
	r, err := zip.OpenReader(src)
	if err != nil {
		return err
	}
	defer r.Close()

	for _, f := range r.File {
		rc, err := f.Open()
		if err != nil {
			return err
		}
		defer rc.Close()

		fpath := filepath.Join(dest, f.Name)
		if f.FileInfo().IsDir() {
			os.MkdirAll(fpath, f.Mode())
		} else {
			var fdir string
			if lastIndex := strings.LastIndex(fpath, string(os.PathSeparator)); lastIndex > -1 {
				fdir = fpath[:lastIndex]
			}

			err = os.MkdirAll(fdir, f.Mode())
			if err != nil {
				log.Fatal(err)
				return err
			}
			f, err := os.OpenFile(
				fpath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
			if err != nil {
				return err
			}
			defer f.Close()

			_, err = io.Copy(f, rc)
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func download(url string, dest string) error {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Printf("Couldn't download file. Try again later (%s)", err)
		return err
	}

	defer resp.Body.Close()
	fmt.Printf("Status code: %s\n", resp.Status)
	if resp.StatusCode != 200 {
		fmt.Println("Returned status code is not 200. Try again later")
		return err
	}

	// Creating output file
	out, err := os.Create(dest)
	if err != nil {
		fmt.Printf("Unexpected error ocurred while creating %s: %s", dest, err)
		return err
	}

	// Writing data
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		fmt.Printf("Unexpected error ocurred while writing data to file: %s", err)
		return err
	}
	out.Close()

	return nil
}

func commandExists(cmd string) bool {
	_, err := exec.LookPath(cmd)
	return err == nil
}

func main() {
	fmt.Println("Starting osu!python installer")

	// Creating temp directory
	if _, err := os.Stat("./osu_python_installer"); os.IsNotExist(err) {
		err := os.Mkdir("./osu_python_installer", os.ModePerm)
		if err != nil {
			fmt.Println("Couldn't create temp directory. Try running as administrator (sudo) or install osu!python manually.")
			return
		}
	} else {
		// Delete latest.zip if exists
		if _, err := os.Stat("./osu_python_installer/latest.zip"); !os.IsNotExist(err) {
			os.Remove("./osu_python_installer/latest.zip")
		}
	}

	// Downloading last version
	fmt.Println("Downloading source")
	// resp, err := http.Get("https://github.com/JustLian/osu-python/releases/latest/download/osu-pytyhon.zip")
	err := download(
		"https://github.com/JustLian/osu-python/releases/latest/download/osu-pytyhon.zip",
		"./osu_python_installer/latest.zip",
	)
	if err != nil {
		fmt.Printf("Couldn't download osu!python code. Try again later (%s)", err)
		return
	}

	// Create game directory
	if _, err := os.Stat("/osu-python"); os.IsNotExist(err) {
		err := os.Mkdir("/osu-python", os.ModePerm)
		if err != nil {
			fmt.Println("Couldn't create game directory. Try running as administrator (sudo) or install osu!python manually.")
			return
		}
	} else {
		// Deleting osu!python from game directory if exists
		if _, err := os.Stat("/osu-python/source"); !os.IsNotExist(err) {
			os.RemoveAll("/osu-python/source")
			err := os.Mkdir("/osu-python/source", os.ModePerm)
			if err != nil {
				fmt.Println("Couldn't create osu!python source directory. Try running as administrator (sudo) or install osu!python manually.")
				return
			}
		}
	}

	// Unpacking files
	fmt.Println("Unpacking source")
	unzip("./osu_python_installer/latest.zip", "/osu-python/source")

	if !commandExists("python") {
		fmt.Println("Downloading Python 3.10.9")

		err = download(
			"https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe",
			"./osu_python_installer/python.exe",
		)
		if err != nil {
			fmt.Printf("Couldn't download Python 3.10.9. Try again later (%s)", err)
			return
		}

		fmt.Println("Installing python")
		cmd := exec.Command("./osu_python_installer/python.exe", "/passive", "PrependPath=1")
		err := cmd.Run()
		if err != nil {
			fmt.Printf("Couldn't install python: %s. Try installing it manually or report this issue to developers: https://github.com/JustLian/osu-python", err)
			return
		}

		for !commandExists("python") {
			time.Sleep(2)
		}
		fmt.Println("Successfully installed python")
	}

	fmt.Println("Installing virtual environment")

	cmd := exec.Command("python", "-m", "venv", "/osu-python/venv")
	err = cmd.Run()
	if err != nil {
		fmt.Printf("Couldn't install virtual environment: %s. Please report this issue to developers: https://github.com/JustLian/osu-python", err)
	}

	fmt.Println("Installing requirements")
	cmd = exec.Command("/osu-python/python/Scripts/python.exe", "-m", "pip", "install", "-r", "/osu-python/source/requirements.txt")
	err = cmd.Run()
	if err != nil {
		fmt.Printf("Couldn't install requirements: %s", err)
		return
	}
	fmt.Println("Game is ready for running. Downloading osu!python.exe")

	err = download("https://github.com/JustLian/osu-python/releases/latest/download/osu!python.exe", "/osu-python/osu!python.exe")
	if err != nil {
		fmt.Printf("Couldn't download osu!python executor application. Try again later (%s)", err)
		return
	}

	fmt.Println("Cleaning up temp folder")
	os.RemoveAll("./osu_python_installer")

	fmt.Println("Installing completed!")
}

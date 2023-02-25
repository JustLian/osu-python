package main

import (
	"archive/zip"
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"strconv"
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

func PrintDownloadPercent(done chan int64, path string, total int64) {

	var stop bool = false

	for {
		select {
		case <-done:
			stop = true
		default:

			file, err := os.Open(path)
			if err != nil {
				log.Fatal(err)
			}

			fi, err := file.Stat()
			if err != nil {
				log.Fatal(err)
			}

			size := fi.Size()

			if size == 0 {
				size = 1
			}

			var percent float64 = float64(size) / float64(total) * 100

			fmt.Printf("%.0f", percent)
			fmt.Println("%")
		}

		if stop {
			break
		}

		time.Sleep(time.Second)
	}
}

func download(url string, dest string) error {

	file := path.Base(url)

	log.Printf("Downloading file %s from %s\n", file, url)

	var path bytes.Buffer
	path.WriteString(dest)
	path.WriteString("/")
	path.WriteString(file)

	start := time.Now()

	out, err := os.Create(path.String())

	if err != nil {
		return err
	}

	defer out.Close()

	headResp, err := http.Head(url)

	if err != nil {
		return err
	}

	defer headResp.Body.Close()

	size, err := strconv.Atoi(headResp.Header.Get("Content-Length"))

	if err != nil {
		return err
	}

	done := make(chan int64)

	go PrintDownloadPercent(done, path.String(), int64(size))

	resp, err := http.Get(url)

	if err != nil {
		return err
	}

	defer resp.Body.Close()

	n, err := io.Copy(out, resp.Body)

	if err != nil {
		return err
	}

	done <- n

	elapsed := time.Since(start)
	log.Printf("Download completed in %s", elapsed)
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
	err := download("https://github.com/JustLian/osu-python/releases/download/v1.0-pre/osu-python.zip", "./osu_python_installer/")
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

	if _, err := os.Stat("/osu-python/bmi"); os.IsNotExist(err) {
		err := os.Mkdir("/osu-python/bmi", os.ModePerm)
		if err != nil {
			fmt.Println("Couldn't create directory for additional beatmapsets pack. Please create folder /osu-python/bmi manually.")
		}
	}

	// Unpacking files
	fmt.Println("Unpacking source")
	unzip("./osu_python_installer/osu-python.zip", "/osu-python/source")

	if !commandExists("python") {
		fmt.Println("Downloading Python 3.10.9")

		err = download(
			"https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe",
			"./osu_python_installer/",
		)
		if err != nil {
			fmt.Printf("Couldn't download Python 3.10.9. Try again later (%s)", err)
			return
		}

		fmt.Println("Installing python")
		cmd := exec.Command("./osu_python_installer/python-3.10.9-amd64.exe", "/passive", "PrependPath=1")
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
	cmd = exec.Command("/osu-python/venv/Scripts/python.exe", "-m", "pip", "install", "-r", "/osu-python/source/requirements.txt")
	err = cmd.Run()
	if err != nil {
		fmt.Printf("Couldn't install requirements: %s", err)
		return
	}
	fmt.Println("Game is ready for running. Downloading osu!python.exe")

	err = download("https://github.com/JustLian/osu-python/releases/download/v1.0-pre/osu!python.exe", "/osu-python/")
	if err != nil {
		fmt.Printf("Couldn't download osu!python executor application. Try downloading it from osu!python latest release page: https://github.com/JustLian/osu-python (%s)\n", err)
	}

	fmt.Println("Cleaning up temp folder")
	os.RemoveAll("./osu_python_installer")

	fmt.Println("Everything is ready, you can launch the game now.\nPLEASE READ: Game will crash if you have less than 18 beatmapsets loaded. If you already have osu! installed use this guide to import your osu! maps into osu!python: https://github.com/JustLian/osu-python/wiki/Game-settings. Otherwise, wait for this download to complete")

	err = download("https://files.catbox.moe/mdjula.zip", "/osu-python/bmi")
	if err != nil {
		fmt.Printf("Couldn't download additional beatmapsets pack. Try again later or download manually from https://files.catbox.moe/mdjula.zip (%s)", err)
		return
	}

	fmt.Println("Installing completed!")
}

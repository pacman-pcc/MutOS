package main

import (
	"bufio"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

const DOWNLOAD_PATH = "/mnt/basic/MutOS/tools"
const GITHUB_REPO = "pacman-pcc/MutRepo"

type ProgressTracker struct {
	io.Reader
	Total   int64
	Current int64
}

func (pt *ProgressTracker) Read(p []byte) (int, error) {
	n, err := pt.Reader.Read(p)
	pt.Current += int64(n)

	if pt.Total > 0 {
		percent := float64(pt.Current) / float64(pt.Total) * 100
		fmt.Printf("\r	Progress: %.1f%% (%d/%d bytes)", percent, pt.Current, pt.Total)
	}
	if err == io.EOF {
		fmt.Println()
	}
	return n, err
}

func downloadFile(url string, fileName string) bool {
	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return false
	}
	req.Header.Set("User-Agent", "Mozilla/5.0")

	resp, err := client.Do(req)
	if err != nil || resp.StatusCode != http.StatusOK {
		return false
	}
	defer resp.Body.Close()

	targetPath := filepath.Join(DOWNLOAD_PATH, fileName)
	out, err := os.Create(targetPath)
	if err != nil {
		fmt.Printf("	[IO-ERROR]: %v\n", err)
		return false
	}
	defer out.Close()

	size := resp.ContentLength
	if size > 0 {
		fmt.Printf("[DOWNLOAD] Streaming %s (%.2f KB)...\n", fileName, float64(size)/1024.0)
	} else {
		fmt.Printf("[DOWNLOAD] Streaming %s (unknown)...\n", fileName)
	}

	progressReader := &ProgressTracker{
		Reader: resp.Body,
		Total:  size,
	}

	_, err = io.Copy(out, progressReader)
	if err != nil {
		return false
	}

	if strings.HasSuffix(fileName, ".py") {
		_ = os.Chmod(targetPath, 0755)
		fmt.Printf("[CHMOD] Executable permissions granted (+x) for %s\n", fileName)
	}

	return true
}

func compileCFILE(fileName string) {
	cPath := filepath.Join(DOWNLOAD_PATH, fileName)
	binaryName := strings.TrimSuffix(fileName, ".c")
	binaryPath := filepath.Join(DOWNLOAD_PATH, binaryName)

	fmt.Printf("[BUILD] Compiling %s using system GCC...\n", fileName)

	cmd := exec.Command("gcc", "-O3", cPath, "-o", binaryPath)
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout

	err := cmd.Run()
	if err != nil {
		fmt.Printf("[BUILD-ERROR] Compilation failed for %s\n", fileName)
		return
	}
	
	_ = os.Remove(cPath)
}

func main() {
	fmt.Printf("[INFO] Target directory set to: %s\n\n", DOWNLOAD_PATH)

	if err := os.MkdirAll(DOWNLOAD_PATH, os.ModePerm); err != nil {
		fmt.Printf("[ERROR] Failed to initialize target directory\n")
		return
	}

	reader := bufio.NewReader(os.Stdin)
	fmt.Print("File is downloading in YAPPI -> ")
	input, _ := reader.ReadString('\n')
	pkgName := strings.TrimRight(input, "\r\n")
	pkgName = strings.TrimSpace(input)

	if pkgName == "" {
		fmt.Println("[ERROR] Package name cannot be empty.")
		return
	}

	extensions := []string{".py", ".c", ".mbf", ""}
	success := false
	startTime := time.Now()

	fmt.Printf("[FETCH] Resolving package %s...\n", pkgName)

	for _, ext := range extensions {
		fileName := pkgName + ext
		url := fmt.Sprintf("https://raw.githubusercontent.com/%s/main/%s", GITHUB_REPO, fileName)

		fmt.Printf("	-> Trying to fetch index for %s\n", fileName)

		if downloadFile(url, fileName) {
			success = true

			if ext == ".c" {
				compileCFILE(fileName)
			}
			break
		}
	}

	if success {
		fmt.Printf("[DONE] Process finished successfully in %s\n", time.Since(startTime).Round(time.Millisecond))
	} else {
		fmt.Printf("[ERROR] Could not find package '%s'\n", pkgName)
	}
}

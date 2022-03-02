package main

import (
	"io"
	"log"
	"os"
	"os/exec"
	"os/signal"
	"syscall"

	"github.com/creack/pty"
	"golang.org/x/term"
)

func test(KUBECONFIG string) error {
	// Create arbitrary command.
	c := exec.Command("bash") //, "-c", "echo $KUBECONFIG")
	c.Env = append(os.Environ(), "KUBECONFIG="+KUBECONFIG)

	// Start the command with a pty.
	ptmx, err := pty.Start(c)
	if err != nil {
		return err
	}

	// Make sure to close the pty at the end.
	defer func() { _ = ptmx.Close() }() // Best effort.
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGWINCH)
	go func() {
		for range ch {
			if err := pty.InheritSize(os.Stdin, ptmx); err != nil {
				log.Printf("error resizing pty: %s", err)
			}
		}
	}()
	ch <- syscall.SIGWINCH                        // Initial resize.
	defer func() { signal.Stop(ch); close(ch) }() // Cleanup signals when done.

	// Set os.Stdin in raw mode.
	oldState, err := term.MakeRaw(int(os.Stdin.Fd()))
	if err != nil {
		panic(err)
	}
	defer func() { _ = term.Restore(int(os.Stdin.Fd()), oldState) }() // Best effort.

	// Copy os.Stdin to the pty and the pty to stdout.
	// NOTE: The goroutine will keep reading until the next keystroke before returning.
	// ptmx.ReadFrom()
	runloop := true
	go func() {
		for runloop {
			data := make([]byte, 1)
			_, err := os.Stdin.Read(data)
			if err != nil {
				log.Printf("error reading from stdin: %s", err)
				return
			}

			_, err = ptmx.Write(data)
			if err != nil {
				log.Printf("error writing to pty: %s", err)
				return
			}
		}
		println("runloop done")
		// _, _ = io.Copy(ptmx, os.Stdin)
	}()
	_, _ = io.Copy(os.Stdout, ptmx)
	runloop = false
	c.Wait()
	ptmx.Write([]byte("\n"))

	return nil
}

func main() {
	println("---")
	if err := test("/home/paul/.kube/configs/adunand.yaml"); err != nil {
		log.Fatal(err)
	}
	println("---")
	if err := test("/home/paul/.kube/configs/cache-reg.yaml"); err != nil {
		log.Fatal(err)
	}
}

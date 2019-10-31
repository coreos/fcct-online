package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
)

const fcct = "./fcct-x86_64-unknown-linux-gnu"

// Variables set via flag
var (
	// debug is if we should be printing out debug logs
	debug bool
	// host is the host to listen on
	host string
	// port is the port to listen on
	port string
)

type postData struct {
	ConfigString string `json:"config_string"`
}

type responseData struct {
	Success        bool                   `json:"success"`
	IgnitionConfig map[string]interface{} `json:"ignition_config"`
	ErrLines       []int                  `json:"err_lines"`
	ErrMsg         string                 `json:"err_msg"`
}

// write the response and sets the status
func writeResponse(w *http.ResponseWriter, res responseData, status int) {
	resJSON, err := json.Marshal(res)
	if err != nil {
		http.Error(*w, "Failed to parse struct `responseData` into JSON object", http.StatusInternalServerError)
	}

	(*w).Header().Set("Content-Type", "application/json")
	(*w).WriteHeader(status)
	(*w).Write(resJSON)
}

// runCommand runs the command and returns the error, stdout, and stderr
func runCommand(command string, input string) (string, string, error) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer
	cmd := exec.Command("bash", "-c", command)
	cmd.Stdin = strings.NewReader(input)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()
	return stdout.String(), stderr.String(), err
}

// logMiddleware produces simple logs when wrapped around a HandlerFunc
func logMiddleware(handler http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("%s - %s - %s", r.RemoteAddr, r.Method, r.URL.Path)
		if debug {
			log.Printf("Request: %+v", r)
		}
		// Execute the original handler
		handler(w, r)
	}
}

// configHandler handles config requests when they come as a POST
func configHandler(w http.ResponseWriter, r *http.Request) {
	// enable CORS
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")

	// note: to enable CORS, it should handle OPTIONS as well
	if r.Method == "OPTIONS" {
		return
	}

	// If it's a POST, process
	if r.Method == "POST" {
		// https://golang.org/pkg/encoding/json/
		// https://golang.org/pkg/os/exec/ (or import the golang code from fcct)

		pd := postData{ConfigString: "default"}
		res := responseData{false, nil, nil, ""}

		contentType := r.Header.Get("Content-type")
		if !strings.Contains(contentType, "application/json") {
			res.ErrMsg = "Content-type must contain 'application/json'"
			log.Printf(res.ErrMsg)
			writeResponse(&w, res, http.StatusBadRequest)
			return
		}

		decoder := json.NewDecoder(r.Body)
		decoder.DisallowUnknownFields()
		err := decoder.Decode(&pd)
		if err != nil {
			log.Println(err)
			res.ErrMsg = fmt.Sprintf("%s", err)
			writeResponse(&w, res, http.StatusInternalServerError)
			return
		}

		// checks if POST json contains a `config_string` key
		if pd.ConfigString == "default" {
			res.ErrMsg = "failed: config_string must be set"
			log.Printf(res.ErrMsg)
			writeResponse(&w, res, http.StatusBadRequest)
			return
		}

		// checks if `config_string` has reasonal length
		maxLen := 31415
		maxLenStr := os.Getenv("ONLINE_FCCT_MAX_LENGTH")
		if len(maxLenStr) > 0 {
			maxLen, _ = strconv.Atoi(maxLenStr)
		}
		if len(pd.ConfigString) > maxLen {
			res.ErrMsg = "failed: FCC string too long"
			log.Printf(res.ErrMsg)
			writeResponse(&w, res, http.StatusBadRequest)
			return
		}

		out, stderr, err := runCommand(fmt.Sprintf("%s", fcct), pd.ConfigString)
		if err != nil {
			log.Println(stderr)
			log.Println(err)

			// errors in the posted Fedora CoreOS Configs
			errorLines := []int{}
			r, _ := regexp.Compile(`[ |\n]*line \d+:`)
			lineNoInfo := r.FindAllString(stderr, -1)
			for _, section := range lineNoInfo {
				n, _ := regexp.Compile(`\d+`)
				s, _ := regexp.Compile(section)
				errorLine, _ := strconv.Atoi(n.FindString(section))
				errorLines = append(errorLines, errorLine)
				stderr = s.ReplaceAllString(stderr, "\n"+strings.TrimSpace(section))
			}

			res.Success = false
			res.ErrMsg = stderr
			res.ErrLines = errorLines
			writeResponse(&w, res, http.StatusOK)
			return
		}

		// otherwise FCCT exits with 0
		// and the stdout has correct FCC
		log.Printf(out)
		log.Printf(stderr)

		var messageJSON map[string]interface{}
		_ = json.Unmarshal([]byte(out), &messageJSON)

		log.Println("Successfully convert to Ignition config")
		res.Success = true
		res.IgnitionConfig = messageJSON
		writeResponse(&w, res, http.StatusOK)
		return
	}

	// Otherwise method is not allowed
	log.Println("Method not allowed")
	http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	return
}

// main is the main entry point on the CLI
func main() {
	flag.BoolVar(&debug, "debug", false, "Enable debug output")
	flag.StringVar(&host, "host", "127.0.0.1", "Host to listen on")
	flag.StringVar(&port, "port", "5000", "Port to listen on")
	flag.Parse()

	// create the host:port string for use
	listenAddress := fmt.Sprintf("%s:%s", host, port)
	if debug {
		log.Printf("Listening on %s", listenAddress)
	}

	// Map /config to our configHandler and wrap it in the log middleware
	http.Handle("/config/", logMiddleware(http.HandlerFunc(configHandler)))

	// Run forever on all interfaces on port 5000
	log.Fatal(http.ListenAndServe(listenAddress, nil))
}

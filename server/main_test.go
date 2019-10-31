package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

// Tests GET request
func TestConfigHandlerGET(t *testing.T) {
	req, err := http.NewRequest("GET", "/config/", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(configHandler)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusMethodNotAllowed)
	}
}

// Tests OPTIONS request
func TestConfigHandlerOPTIONS(t *testing.T) {
	req, err := http.NewRequest("OPTIONS", "/config/", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(configHandler)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}
}

// Tests POST with non-json content type in header
func TestConfigHandlerNonJSONHeader(t *testing.T) {
	body := fmt.Sprintf(`
	{
		"config_string": "variant: fcos\nversion: 1.0.0"
	}
	`)
	req, err := http.NewRequest("POST", "/config/", strings.NewReader(body))
	req.Header.Set("Content-type", "text/plain")
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(configHandler)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		b, _ := ioutil.ReadAll(rr.Body)
		t.Errorf("response body: %v", string(b))
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusBadRequest)
	}
}

// Tests POST with json content type, but content is not json
func TestConfigHandlerNonJSONBody(t *testing.T) {
	body := fmt.Sprintf(`
	{
		"config_string": "variant: fcos\nversion: 1.0.0"

	`)
	req, err := http.NewRequest("POST", "/config/", strings.NewReader(body))
	req.Header.Set("Content-type", "application/json")
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(configHandler)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusInternalServerError {
		b, _ := ioutil.ReadAll(rr.Body)
		t.Errorf("response body: %v", string(b))
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusInternalServerError)
	}
}

// Tests POST with json content type, but no `config_string` key
func TestConfigHandlerNoKey(t *testing.T) {
	body := fmt.Sprintf(`
	{
	}`)
	req, err := http.NewRequest("POST", "/config/", strings.NewReader(body))
	req.Header.Set("Content-type", "application/json")
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(configHandler)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		b, _ := ioutil.ReadAll(rr.Body)
		t.Errorf("response body: %v", string(b))
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusBadRequest)
	}
}

// Tests POST with json content type, but with more than maxLen content
func TestConfigHandlerMaxLength(t *testing.T) {
	maxLen := 31415
	body := fmt.Sprintf(`
	{
		"config_string": "%s"
	}`, strings.Repeat("w", maxLen+1))
	req, err := http.NewRequest("POST", "/config/", strings.NewReader(body))
	req.Header.Set("Content-type", "application/json")
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(configHandler)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		b, _ := ioutil.ReadAll(rr.Body)
		t.Errorf("response body: %v", string(b))
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusBadRequest)
	}
}

// Tests POST with json content type, but FCCT exits with non-zero
func TestConfigHandlerSuccessWithError(t *testing.T) {
	body := fmt.Sprintf(`
	{
		"config_string": "variant: fcos"

	}`)
	req, err := http.NewRequest("POST", "/config/", strings.NewReader(body))
	req.Header.Set("Content-type", "application/json")
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(configHandler)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusOK {
		b, _ := ioutil.ReadAll(rr.Body)
		t.Errorf("response body: %v", string(b))
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusInternalServerError)
	}
}

// Tests POST with json content type and FCCT exits with zero
func TestConfigHandlerSuccess(t *testing.T) {
	body := fmt.Sprintf(`
	{
		"config_string": "variant: fcos\nversion: 1.0.0"

	}`)
	req, err := http.NewRequest("POST", "/config/", strings.NewReader(body))
	req.Header.Set("Content-type", "application/json")
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(configHandler)

	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusOK {
		b, _ := ioutil.ReadAll(rr.Body)
		t.Errorf("response body: %v", string(b))
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusInternalServerError)
	}
}

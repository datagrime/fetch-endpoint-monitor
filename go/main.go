package main

import (
	"context"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"os/signal"
	"strings"
	"sync"
	"time"

	"gopkg.in/yaml.v3"
)

type EndpointConfig struct {
	Name    string            `yaml:"name"`
	URL     string            `yaml:"url"`
	Method  string            `yaml:"method,omitempty"`
	Headers map[string]string `yaml:"headers,omitempty"`
	Body    string            `yaml:"body,omitempty"`
	Domain  string            `yaml:"-"`
}

type DomainStats struct {
	Total int
	Up    int
}

func main() {
	if len(os.Args) > 2 {
		fmt.Println("Usage: ./monitor [config-file]")
		os.Exit(1)
	}

	configFile := "endpoint.yaml"
	if len(os.Args) == 2 {
		configFile = os.Args[1]
	}

	endpoints, err := loadConfig(configFile)
	if err != nil || len(endpoints) == 0 {
		fmt.Printf("Error loading config or no valid endpoints: %v\n", err)
		os.Exit(1)
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Handle CTRL+C (SIGINT) for graceful shutdown
	signalChan := make(chan os.Signal, 1)
	signal.Notify(signalChan, os.Interrupt)
	go func() {
		<-signalChan
		fmt.Println("\nReceived interrupt, shutting down...")
		cancel()
	}()

	monitorEndpoints(ctx, endpoints)
}

func loadConfig(filename string) ([]EndpointConfig, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var endpoints []EndpointConfig
	if err := yaml.Unmarshal(data, &endpoints); err != nil {
		return nil, err
	}

	validEndpoints := make([]EndpointConfig, 0, len(endpoints))
	seenDomains := make(map[string]bool)

	for _, ep := range endpoints {
		if ep.URL == "" || ep.Name == "" {
			continue
		}
		if ep.Method == "" {
			ep.Method = http.MethodGet
		}

		u, err := url.Parse(ep.URL)
		if err != nil {
			continue
		}
		ep.Domain = u.Hostname()

		if !seenDomains[ep.Domain] {
			seenDomains[ep.Domain] = true
		}

		validEndpoints = append(validEndpoints, ep)
	}

	return validEndpoints, nil
}

func monitorEndpoints(ctx context.Context, endpoints []EndpointConfig) {
	var stats sync.Map
	domainOrder := getDomainOrder(endpoints)
	ticker := time.NewTicker(15 * time.Second)
	defer ticker.Stop()

	for range ticker.C {
		select {
		case <-ctx.Done():
			return
		default:
			wg := sync.WaitGroup{}
			results := make(chan CheckResult, len(endpoints))

			for _, ep := range endpoints {
				wg.Add(1)
				go func(ep EndpointConfig) {
					defer wg.Done()
					results <- CheckResult{Domain: ep.Domain, Up: checkEndpoint(ep)}
				}(ep)
			}

			// Close results channel when all checks are done
			go func() {
				wg.Wait()
				close(results)
			}()

			// Collect results and update stats
			for result := range results {
				stat, _ := stats.LoadOrStore(result.Domain, &DomainStats{})
				d := stat.(*DomainStats)
				d.Total++
				if result.Up {
					d.Up++
				}
			}

			printStats(&stats, domainOrder)
		}
	}
}

type CheckResult struct {
	Domain string
	Up     bool
}

func checkEndpoint(ep EndpointConfig) bool {
	client := &http.Client{Timeout: 5 * time.Second}

	var req *http.Request
	var err error
	start := time.Now()

	if ep.Body != "" {
		body := strings.NewReader(ep.Body)
		req, err = http.NewRequest(ep.Method, ep.URL, body)
		if err != nil {
			return false
		}
		if _, exists := ep.Headers["Content-Type"]; !exists {
			req.Header.Set("Content-Type", "application/json")
		}
	} else {
		req, err = http.NewRequest(ep.Method, ep.URL, nil)
		if err != nil {
			return false
		}
	}

	for k, v := range ep.Headers {
		req.Header.Set(k, v)
	}

	resp, err := client.Do(req)
	if err != nil {
		return false
	}
	defer resp.Body.Close()

	latency := time.Since(start).Milliseconds()
	return resp.StatusCode >= 200 && resp.StatusCode < 300 && latency < 500
}

func getDomainOrder(endpoints []EndpointConfig) map[string]int {
	order := make(map[string]int)
	index := 0
	for _, ep := range endpoints {
		if _, exists := order[ep.Domain]; !exists {
			order[ep.Domain] = index
			index++
		}
	}
	return order
}

func printStats(stats *sync.Map, order map[string]int) {
	domains := make([]string, len(order))
	for domain, index := range order {
		domains[index] = domain
	}

	for _, domain := range domains {
		stat, ok := stats.Load(domain)
		if !ok {
			fmt.Printf("%s has 0%% availability percentage\n", domain)
			continue
		}

		s := stat.(*DomainStats)
		if s.Total == 0 {
			fmt.Printf("%s has 0%% availability percentage\n", domain)
		} else {
			percent := float64(s.Up) / float64(s.Total) * 100
			fmt.Printf("%s has %.0f%% availability percentage\n", domain, percent)
		}
	}
}

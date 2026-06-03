package main

import (
	"encoding/json"
	"flag"
	"os"
	"path/filepath"
	"sort"

	"fog.local/resume/internal/f5"
)

func main() {
	outPath := flag.String("out", "/app/output/resume-audit.json", "output path")
	root := flag.String("root", "/app", "workspace root")
	oneCase := flag.String("case", "", "single case")
	flag.Parse()

	names := f5.AllCases()
	if *oneCase != "" {
		names = []string{*oneCase}
	}
	sort.Strings(names)
	report := f5.Report{Cases: []f5.CaseResult{}}
	for _, name := range names {
		result, err := f5.RunRow(*root, name)
		if err != nil {
			panic(err)
		}
		report.Cases = append(report.Cases, result)
	}
	if err := os.MkdirAll(filepath.Dir(*outPath), 0o755); err != nil {
		panic(err)
	}
	encoded, err := json.MarshalIndent(report, "", "  ")
	if err != nil {
		panic(err)
	}
	if err := os.WriteFile(*outPath, append(encoded, '\n'), 0o644); err != nil {
		panic(err)
	}
}

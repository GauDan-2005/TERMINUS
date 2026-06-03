package exec

import "fog.local/resume/internal/sim"

type World = sim.World
type Hostile = sim.Hostile
type EffectState = sim.EffectState
type Profile = sim.Profile
type MoveRow = sim.MoveRow
type PathSummary = sim.PathSummary
type VisPair = sim.VisPair
type EffectRow = sim.EffectRow
type CaseResult = sim.CaseResult
type Report = sim.Report
type ScriptStep = sim.ScriptStep

func ProfileFor(name string) Profile { return sim.ProfileFor(name) }
func AllCases() []string             { return sim.AllCases() }
func LoadLayout(root, name string) (*World, error) {
	return sim.LoadLayout(root, name)
}
func LoadScript(root, name string) ([]ScriptStep, error) {
	return sim.LoadScript(root, name)
}
func LoadRadius(root, name string) (int, error) { return sim.LoadRadius(root, name) }

package h7

type Counter struct {
	Runs int
}

func Bump(c *Counter) {
	c.Runs++
}

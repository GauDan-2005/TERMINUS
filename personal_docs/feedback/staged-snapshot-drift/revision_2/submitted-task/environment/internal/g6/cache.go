package g6

type Cache struct {
	Items []string
}

func phase_a(c *Cache, value string) {
	c.Items = append(c.Items, value)
}

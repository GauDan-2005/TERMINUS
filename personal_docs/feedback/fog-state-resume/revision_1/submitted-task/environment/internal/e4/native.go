package e4

/*
#cgo CFLAGS: -I${SRCDIR}/../../probe
#include <stdlib.h>
#include "legality.h"
#include "../../probe/legality.c"
*/
import "C"
import (
	"fog.local/resume/internal/sim"
	"unsafe"
)

func StepLegal(w *sim.World, x0, y0, x1, y1 int) bool {
	n := w.Width * w.Height
	buf := C.malloc(C.size_t(n) * C.size_t(unsafe.Sizeof(C.int(0))))
	if buf == nil {
		return false
	}
	defer C.free(buf)
	grid := (*[1 << 30]C.int)(buf)[:n:n]
	for i, wall := range w.Walls {
		if wall {
			grid[i] = 1
		}
	}
	ctx := C.struct_qx{width: C.int(w.Width), height: C.int(w.Height), grid: (*C.int)(buf)}
	return C.walk_e(&ctx, C.int(x0), C.int(y0), C.int(x1), C.int(y1)) == 1
}

// Code generated by "stringer -type HandCardState -linecomment"; DO NOT EDIT.

package joerg

import "strconv"

func _() {
	// An "invalid array index" compiler error signifies that the constant values have changed.
	// Re-run the stringer command to generate them again.
	var x [1]struct{}
	_ = x[VisibleOnlyForPlayer-0]
	_ = x[VisibleForEveryone-1]
	_ = x[HiddenFromEveryone-2]
}

const _HandCardState_name = "VisibleOnlyForPlayerVisibleForEveryoneHiddenFromEveryone"

var _HandCardState_index = [...]uint8{0, 20, 38, 56}

func (i HandCardState) String() string {
	if i < 0 || i >= HandCardState(len(_HandCardState_index)-1) {
		return "HandCardState(" + strconv.FormatInt(int64(i), 10) + ")"
	}
	return _HandCardState_name[_HandCardState_index[i]:_HandCardState_index[i+1]]
}

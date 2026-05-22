"""Pointer calibration helpers for camera-to-screen mapping."""

from desktop_control_prototype.config import (
    POINTER_FLIP_X,
    POINTER_FLIP_Y,
    POINTER_X_MAX,
    POINTER_X_MIN,
    POINTER_Y_MAX,
    POINTER_Y_MIN,
)


def _clamp(value, minimum=0.0, maximum=1.0):
    return max(minimum, min(maximum, value))


def calibrate_pointer(x_norm, y_norm):
    x = _clamp(x_norm)
    y = _clamp(y_norm)

    if POINTER_FLIP_X:
        x = 1.0 - x
    if POINTER_FLIP_Y:
        y = 1.0 - y

    x_span = POINTER_X_MAX - POINTER_X_MIN
    y_span = POINTER_Y_MAX - POINTER_Y_MIN

    x = POINTER_X_MIN + (x * x_span)
    y = POINTER_Y_MIN + (y * y_span)

    return _clamp(x), _clamp(y)
"""Gesture interpretation stubs."""
def interpret(landmarks):
    """Map landmarks to a simple gesture label string.

    This is a stub: real implementation should analyze fingertip positions
    and motion over time.
    """
    if not landmarks:
        return "None"
    # Very naive rule: if index finger (8) y is less than thumb (4) -> pointing
    try:
        idx = landmarks[8]
        thumb = landmarks[4]
        if idx[1] < thumb[1]:
            return "Pointing"
    except Exception:
        pass
    return "Unknown"

"""Simple confirmation manager for safety-critical actions."""


class ConfirmManager:
    def __init__(self, required: bool = False, timeout: float = 2.0, confirm_gesture: str = "Open_Palm"):
        self.required = required
        self.timeout = timeout
        self.confirm_gesture = confirm_gesture
        self.pending_action = None
        self.pending_since = 0.0

    def request(self, action: str, now: float) -> str:
        """Request confirmation for `action` at time `now`.

        Returns:
          - "confirmed": action should proceed
          - "pending": action registered; needs repeat to confirm
        """
        if not self.required:
            return "confirmed"

        if self.pending_action == action and now - self.pending_since <= self.timeout:
            self.pending_action = None
            self.pending_since = 0.0
            return "confirmed"

        # register pending confirmation
        self.pending_action = action
        self.pending_since = now
        return "pending"

    def cancel_if_expired(self, now: float) -> None:
        if self.pending_action and now - self.pending_since > self.timeout:
            self.pending_action = None
            self.pending_since = 0.0

    def confirm_with_gesture(self, gesture: str, now: float) -> bool:
        """Confirm the pending action using a gesture. Returns True if confirmed."""
        if not self.required or not self.pending_action:
            return False
        self.cancel_if_expired(now)
        if not self.pending_action:
            return False
        if gesture != self.confirm_gesture:
            return False
        self.pending_action = None
        self.pending_since = 0.0
        return True

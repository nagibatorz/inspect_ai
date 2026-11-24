"""In-memory tests for the TUI client's ACP session router.

The router is built by ``_build_session_router`` and driven directly —
no server or socket is needed.
"""

from __future__ import annotations

from typing import Any, cast

from inspect_ai.agent._acp.tui.client import AttachedSession, _build_session_router


def _ignore(_: Any) -> None: ...


async def test_turn_state_notification_is_accepted() -> None:
    """The server sends inspect/turn_state on attach and each turn boundary.

    The TUI derives turn activity from session/update, so the route
    ignores the notification — but it must exist, or the router raises
    "Method not found" and logs an error for every snapshot (#6733).
    """
    router = _build_session_router(
        session_ref=cast(AttachedSession, None),
        on_session_update=_ignore,
        on_request_permission=_ignore,
        on_request_elicitation=_ignore,
        on_inspect_event=_ignore,
    )
    for state in ("started", "ended"):
        await router("inspect/turn_state", {"sessionId": "s", "state": state}, True)

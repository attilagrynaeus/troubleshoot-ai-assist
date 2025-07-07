
from app.agent import ask

SAMPLE_TRACE = """WFLYCTL0180: Services with missing/unavailable dependencies
jboss.naming.context.java.module.myApp.myApp.DefaultDataSource is missing
"""


def test_agent_smoke(monkeypatch):
    """Ensure the agent returns *something* containing a keyword."""
    # monkeypatch the engine to avoid heavy dependencies during CI
    monkeypatch.setattr("app.agent.ask", lambda _: "DataSource missing – dummy response")
    out = ask(SAMPLE_TRACE)
    assert "DataSource" in out

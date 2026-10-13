from agno.os import AgentOS
from teams.miko import miko_team
from agents.lumi import lumi
from agents.dakdak import dakdak
from agents.kiko import kiko
from agents.nobi import nobi

miko_os = AgentOS(
    id="MIKO-OS",
    description="MIKO AgentOS",
    teams=[miko_team],
    agents=[lumi, dakdak, kiko, nobi],
    cors_allowed_origins=[
        "http://127.0.0.1:8765",
        "http://localhost:8765",
    ],
)

app = miko_os.get_app()

if __name__ == "__main__":
    miko_os.serve(app="server:app", reload=True)

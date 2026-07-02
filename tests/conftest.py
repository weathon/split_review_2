import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))

# main.py calls weave.init at import time (hits wandb servers); stub it out so
# tests never touch the network.
weave_stub = types.ModuleType("weave")
weave_stub.init = lambda *args, **kwargs: None
sys.modules["weave"] = weave_stub

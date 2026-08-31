import os
import tempfile
from pathlib import Path

TEST_HOME = Path(tempfile.mkdtemp(prefix="fca-tests-"))
os.environ["FCA_HOME"] = str(TEST_HOME)

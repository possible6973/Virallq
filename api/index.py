import sys
from pathlib import Path

# Add root directory to path so imports work seamlessly
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from api_server import app

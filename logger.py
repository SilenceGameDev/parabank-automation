import logging
import sys
from pathlib import Path
from rich.logging import RichHandler

logger = logging.getLogger(__name__)

# Some characters can't be read by default so adding utf-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

# the handler determines where the log go: stdout/file
shell_handler = RichHandler() # shows logs in shell

# used to configure the level to send out
logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.INFO)
# note if logger.setLevel is set to a higher level than the handler, that handler will not be able to access any log lower than that level. Ex: if logger is set to CRITICAL then handler is set to Warning the handler will NOT see any logs below CRITICAL.

# the formatter determines what our logs will look like
fmt_shell = "%(message)s"

shell_formatter = logging.Formatter(fmt_shell)

# here we hook everything together
shell_handler.setFormatter(shell_formatter)

logger.addHandler(shell_handler)

log_path = Path(__file__).resolve().parent / "debug.log"
file_handler = logging.FileHandler(filename=log_path, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
fmt_file = "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
file_formatter = logging.Formatter(fmt_file)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
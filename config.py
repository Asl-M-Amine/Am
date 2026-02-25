from typing import Tuple, Dict, Optional
from renderer import get_42_pattern_coords


class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass


class Config:
    """Configuration container."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: Optional[int] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed


# ===============================
# Helpers
# ===============================

def parse_coords(value: str) -> Tuple[int, int]:
    """Parse coordinates x,y."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(f"Coordinates must be in format x,y: '{value}'")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        raise ConfigError(f"Coordinates must be integers: '{value}'")


def parse_bool(value: str, key_name: str) -> bool:
    val = value.lower()
    if val == "true":
        return True
    if val == "false":
        return False
    raise ConfigError(f"{key_name} must be True or False")


def validate_config(config: Config) -> None:
    """Validate configuration values."""

    # Required fields
    required = ["width", "height", "entry", "exit", "output_file", "perfect"]
    for name in required:
        if getattr(config, name) is None:
            raise ConfigError(f"Missing required parameter: {name}")

    # Size validation
    if config.width <= 0 or config.height <= 0:
        raise ConfigError("Width and height must be positive")

    if config.width < 9 or config.height < 7:
        raise ConfigError("Maze too small (minimum 9x7)")

    # Coordinates inside bounds
    ex, ey = config.entry
    ox, oy = config.exit

    if not (0 <= ex < config.width and 0 <= ey < config.height):
        raise ConfigError(f"Entry coordinates out of bounds: {config.entry}")

    if not (0 <= ox < config.width and 0 <= oy < config.height):
        raise ConfigError(f"Exit coordinates out of bounds: {config.exit}")

    # Entry != Exit
    if config.entry == config.exit:
        raise ConfigError("Entry and exit must be different")

    # Output file validation
    if not config.output_file or config.output_file.strip() == "":
        raise ConfigError("OUTPUT_FILE cannot be empty")
    if config.output_file in (".", "..", "./", "../", "/"):
        raise ConfigError("OUTPUT_FILE cannot be a directory")
    if "/" in config.output_file and config.output_file.endswith("/"):
        raise ConfigError("Invalid output filename")
    if not config.output_file.endswith(".txt"):
        print("\033[33mWarning: output file should be .txt\033[0m")

    # 42 pattern checks
    if config.width >= 9 and config.height >= 7:
        p42 = get_42_pattern_coords(config.width, config.height)
        if config.entry in p42:
            raise ConfigError("Entry cannot be inside 42 pattern")
        if config.exit in p42:
            raise ConfigError("Exit cannot be inside 42 pattern")


# ===============================
# Loader
# ===============================

def load_config(filename: str) -> Config:
    """Load configuration file safely."""

    config_data: Dict[str, str] = {}
    valid_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
        "PERFECT", "SEED"
    }

    try:
        with open(filename, "r") as f:
            for lineno, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigError(f"Invalid line {lineno}: missing '='")
                if line.count("=") != 1:
                    raise ConfigError(f"Invalid line {lineno}: too many '='")
                key, value = map(str.strip, line.split("=", 1))
                key = key.upper()
                if key not in valid_keys:
                    raise ConfigError(f"Unsupported key '{key}' on "
                                      f"line {lineno}")
                config_data[key] = value
    except FileNotFoundError:
        raise ConfigError(f"Config file '{filename}' not found")
    except PermissionError:
        raise ConfigError(f"Cannot access config file '{filename}' "
                          "(permission denied)")

    # Parse numeric fields
    try:
        width = int(config_data["WIDTH"])
    except KeyError:
        raise ConfigError("Missing WIDTH")
    except ValueError:
        raise ConfigError("WIDTH must be an integer")

    try:
        height = int(config_data["HEIGHT"])
    except KeyError:
        raise ConfigError("Missing HEIGHT")
    except ValueError:
        raise ConfigError("HEIGHT must be an integer")

    try:
        entry = parse_coords(config_data["ENTRY"])
    except KeyError:
        raise ConfigError("Missing ENTRY")

    try:
        exit_ = parse_coords(config_data["EXIT"])
    except KeyError:
        raise ConfigError("Missing EXIT")

    try:
        output_file = config_data["OUTPUT_FILE"]
    except KeyError:
        raise ConfigError("Missing OUTPUT_FILE")

    # Booleans
    try:
        perfect = parse_bool(config_data["PERFECT"], "PERFECT")
    except KeyError:
        raise ConfigError("Missing PERFECT")

    # Seed
    seed: Optional[int] = None
    if "SEED" in config_data and config_data["SEED"].strip() != "":
        try:
            seed = int(config_data["SEED"])
        except ValueError:
            raise ConfigError("SEED must be an integer")

    cfg = Config(width, height, entry, exit_, output_file, perfect, seed)
    validate_config(cfg)
    return cfg

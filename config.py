class ConfigError(Exception):
    pass


class Config:
    def __init__(self, width, height, entry, exit, output_file, perfect, seed):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed


def load_config(filename):
    config_data = {}

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ConfigError(f"Invalid line: {line}")

                key, value = line.split("=", 1)
                config_data[key.strip()] = value.strip()

    except FileNotFoundError:
        raise ConfigError("Config file not found")

    try:
        width = int(config_data["WIDTH"])
        height = int(config_data["HEIGHT"])

        entry = tuple(map(int, config_data["ENTRY"].split(",")))
        exit = tuple(map(int, config_data["EXIT"].split(",")))

        output_file = config_data.get("OUTPUT_FILE", None)

        perfect_str = config_data.get("PERFECT", "True")
        perfect = perfect_str.lower() == "true"

        seed_str = config_data.get("SEED", None)
        seed = int(seed_str) if seed_str is not None else None

    except KeyError as e:
        raise ConfigError(f"Missing configuration: {e}")

    return Config(width, height, entry, exit, output_file, perfect, seed)

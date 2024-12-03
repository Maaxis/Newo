class Permissions:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)

    def load_config(self, file_path):
        config = {}
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key_path, value = line.split('=', 1)
                    value = value.strip()
                    keys = key_path.split('.')
                    current_dict = config
                    for key in keys[:-1]:
                        if key not in current_dict:
                            current_dict[key] = {}
                        current_dict = current_dict[key]
                    current_dict[keys[-1]] = value
        return config

    def convert_value(self, value):
        """Convert string values to appropriate data types."""
        if value.upper() == 'TRUE':
            return True
        elif value.upper() == 'FALSE':
            return False
        return value

    def get(self, path):
        """Retrieve a configuration value by specifying its path in dot notation."""
        keys = path.split('.')
        current_value = self.config
        for key in keys:
            current_value = current_value.get(key)
            if current_value is None:
                return None
        return self.convert_value(current_value)

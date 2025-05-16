import argparse
import yaml
from pathlib import Path
from typing import Any, Optional


class ConfigArgumentParser(argparse.ArgumentParser):
    """
    Extended ArgumentParser that supports loading arguments from YAML config files.
    Class Attributes:
        _config_flag_attr (str): The name of the argument flag used to specify the config file path (defaults to "config").
            This will be used in command line arguments as --config.

        _config_path (Optional[Path]): Internal storage for the path to the configuration file
            after it's been parsed from arguments. Will be None if no config file was specified.
    """
    _config_flag_attr: str = "config"
    _config_path: Optional[Path] = None

    def _load_config(self) -> dict:
        """Load and parse the YAML config file."""
        config_file = self._config_path
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found at: {self._config_path}")
        with open(config_file, "r", encoding="utf-8") as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML format in config file: {e}")

    def _get_action_for_key(self, key: str) -> Optional[argparse.Action]:
        """Get the corresponding Action for a config key."""
        return next(
            (action for action in self._actions if action.dest == key),
            None
        )

    def _apply_config_value(
        self,
        action: Optional[argparse.Action],
        key: str,
        value: Any,
        parsed_args: argparse.Namespace
    ):
        """Apply a config value to parsed arguments with type conversion."""
        if action and action.type is not None:
            try:
                converted_value = action.type(value)
                setattr(parsed_args, key, converted_value)
            except (ValueError, TypeError) as e:
                self.error(
                    f"Invalid value '{value}' for argument '{key}' in config file. "
                    f"Expected type: {action.type.__name__}. Error: {str(e)}"
                )
        else:
            setattr(parsed_args, key, value)

    def parse_args(
            self,
            args: Optional[list[str]] = None,
            namespace: Optional[argparse.Namespace] = None
    ) -> argparse.Namespace:
        """
        Parse command line arguments and optionally load from config file.
        """
        parsed_args = super().parse_args(args, namespace)


        config_flag_attr = getattr(parsed_args, self._config_flag_attr, None)
        if config_flag_attr is not None:
            self._config_path = Path(getattr(parsed_args, self._config_flag_attr))

        if self._config_path is not None:
            config_data = self._load_config()
            for key, value in config_data.items():
                action = self._get_action_for_key(key)
                self._apply_config_value(action, key, value, parsed_args)

        return parsed_args

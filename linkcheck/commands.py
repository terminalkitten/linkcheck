import asyncio
from pathlib import Path
from typing import Any, List, Optional, Union

import click
import toml
from pydantic import BaseModel
from pyfiglet import Figlet

from linkcheck.django import run_link_checker

font = Figlet(font="slant")

from linkcheck import __version__ as VERSION


class CommandLineArgs(BaseModel):
    mode: Optional[str]
    hostname: Optional[str]
    config: str = "linkcheck.toml"


class ConfigFile(BaseModel):
    mode: Optional[str]
    login_url_path: Optional[str] = "login"
    config: str = "linkcheck.toml"
    hostname: Optional[str]
    user: str


def load_settings(file_path: str) -> Union[Any, dict[str, Any]]:
    path = Path(file_path)
    if path.is_file():
        with open("linkcheck.toml", "r") as config_file:
            return toml.loads(config_file.read())


class LinkCheck:
    def __init__(self, **kwargs):
        # Get commandline arguments
        self.args = CommandLineArgs(**kwargs)
        # Get toml file settings
        self.toml_config = load_settings(self.args.config)
        # Merge commandline args with presedent over toml file args, except if there None
        filtered_args = {k: v for k, v in self.args.dict().items() if v is not None}
        self.config = ConfigFile(**{**self.toml_config, **filtered_args})

    def run(self) -> None:
        asyncio.run(run_link_checker(self.config))

    def show_version(self) -> None:
        click.secho("LinkCheck CLI tools")
        click.secho(font.renderText("LinkCheck"), fg="yellow")
        click.secho(f"Version {VERSION}")


pass_linkcheck = click.make_pass_decorator(LinkCheck, ensure=True)

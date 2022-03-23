import asyncio
from pathlib import Path
from typing import Any, List, Optional, Union

import click
import toml
from pydantic import BaseModel
from pyfiglet import Figlet

from linkcheck.django import link_checker_browser, link_checker_visit

font = Figlet(font="slant")

from linkcheck import __version__ as VERSION


class CommandLineArgs(BaseModel):
    config: str = "linkcheck.toml"
    mode: Optional[str]

    hostname: Optional[str]
    entry_point: Optional[str]
    login_url_path: Optional[str] = "login"


class ConfigFile(CommandLineArgs):
    users: List[dict[str, str]]


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

    def visit(self) -> None:
        asyncio.run(link_checker_visit(self.config))

    def browser(self) -> None:
        asyncio.run(link_checker_browser(self.config))

    def show_version(self) -> None:
        click.secho("LinkCheck CLI tools")
        click.secho(font.renderText("LinkCheck"), fg="yellow")
        click.secho(f"Version {VERSION}")


pass_linkcheck = click.make_pass_decorator(LinkCheck, ensure=True)

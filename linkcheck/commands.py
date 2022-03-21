import click
from pathlib import Path
from pyfiglet import Figlet

from typing import List, Any, Union, Optional
from pydantic import BaseModel
import toml

from linkcheck.django import login

font = Figlet(font='slant')

from linkcheck import __version__ as VERSION


class CommandLineArgs(BaseModel):
    mode: Optional[str]
    hostname: Optional[str]
    config: Optional[str]


class ConfigFile(BaseModel):
    mode: Optional[str]
    login_url_path: Optional[str] = "login"


def load_settings(file_path: str) -> Union[Any, ConfigFile]:
    path = Path(file_path)
    if path.is_file():
        with open('linkcheck.toml', 'r') as config_file:
            return ConfigFile(**toml.loads(config_file.read()))


class LinkCheck:
    def __init__(self, **kwargs):
        self.__version__ = "0.3.2"
        self.args = CommandLineArgs(**kwargs)
        self.config = load_settings(self.args.config)

    def show_version(self) -> None:
        click.secho("LinkCheck CLI tools")
        click.secho(font.renderText('LinkCheck'), fg='yellow')
        click.secho(f"Version {VERSION}")


pass_linkcheck = click.make_pass_decorator(LinkCheck, ensure=True)

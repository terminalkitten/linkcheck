import click

from linkcheck.commands import LinkCheck, pass_linkcheck


@click.group()
@click.option("--config", default="linkcheck.toml", help="select config file")
@click.pass_context
def cli(ctx, **kwargs):
    """linkcheck command line tool"""
    ctx.obj = LinkCheck(**kwargs)


@cli.command("version", short_help="show linkcheck version")
@pass_linkcheck
def version(linkcheck):
    linkcheck.show_version()


if __name__ == "__main__":
    cli()

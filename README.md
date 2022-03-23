Intro with some text [Read the docs](https://linkcheck.readthedocs.io/en/latest/).

## Features

Some of it’s stand out features are:

- Check all links in Django project from user perspective.
- Check links with plain http call or with full browser request.
- 

## Installation

Installing with:

```bash
pip install 'linkcheck'
```

##  Setup

Add a `linkcheck.toml` to project directory, so linkcheck can pick-up settings.

```toml
hostname = "http://localhost:8000"
entry_point = "/dashboard"

[[users]]
username = "admin"
password = "admin123"
```

## Usage

```
Usage: linkcheck [OPTIONS] COMMAND [ARGS]...

  Django linkcheck command line tool

Options:
  --config TEXT  select config file
  --help         Show this message and exit.

Commands:
  browser  run linkcheck in browser-mode
  version  show linkcheck version
  visit    run linkcheck in visit-mode
```

## Documentation

Our documentation is on [Read the docs](https://linkcheck.readthedocs.io/en/latest/linkcheck/getting_started/index.html).

## License

The MIT License
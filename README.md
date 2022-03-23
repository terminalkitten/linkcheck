Intro with some text [Read the docs](https://linkcheck.readthedocs.io/en/latest/).

## Features

Some of it’s stand out features are:

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
linkcheck visit

linkcheck browser
```

## Documentation

Our documentation is on [Read the docs](https://linkcheck.readthedocs.io/en/latest/linkcheck/getting_started/index.html).

## License

The MIT License
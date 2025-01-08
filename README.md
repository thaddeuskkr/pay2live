# pay2live

## Development Setup

**This project is managed using [`uv`](https://github.com/astral-sh/uv).**  
**`uv`** is an extremely fast Python package and project manager, written in Rust.

**Additionally, developing this project requires Node.js.**  
This project uses some `npm` modules for development, namely `tailwindcss` and `prettier`. Tailwind CSS is a CSS framework packed with classes that produce an output CSS, which the HTML files import. Prettier is used for code formatting.

### Install a package manager

```sh
# On Windows, use Scoop.
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

```sh
# On MacOS, use Homebrew.
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```sh
# Most Linux distributions include a package manager.
# Therefore, isntructions for this won't be found here.
```

### Install [`uv`](https://github.com/astral-sh/uv) and [`node.js`](https://nodejs.org)

```sh
# On Windows, using Scoop
scoop install git aria2 uv nodejs
```

```sh
# On MacOS, using Homebrew
brew install uv node
```

```sh
# If you're using Linux, you can figure this out yourself. But here you go anyways.
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
nvm install node
```

### Clone the repository and install the required dependencies

```sh
git clone https://github.com/thaddeuskkr/pay2live.git
cd pay2live
npm install
uv sync
```

## Run the development server(s)

_Do these in separate terminals, as they are blocking processes._

### Run Tailwind CSS (watch mode)

```sh
npm run watch
```

### Run the Flask application

```sh
uv run flask run
```

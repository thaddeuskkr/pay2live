# pay2live

**pay2live** is a web application designed to optimize patient management for small clinics. It simplifies appointment booking, queue management, administrative tasks, and online store operations while integrating WhatsApp for OTP-based authentication and patient notifications.

## Live Demo

*This web application is currently running live at [pay2live.tkkr.dev](https://pay2live.tkkr.dev)*

## Features

- **Appointment Booking & Queue Management** – Streamlined patient scheduling and real-time queue updates.
- **Administrative Dashboard** – Manage users, appointments, and clinic operations with ease.
- **WhatsApp Integration** – OTP-based login and automated patient notifications.
- **Online Store with Cart Functionality** – Enables clinics to offer products/services online.
- **Role-Based Access Control** – Secure user management and authentication.
- **Cloud Deployment with Docker & GitHub Actions** – Automated builds and seamless updates.

## Stack

- **Backend:** Flask, Jinja, MongoDB
- **Frontend:** HTML, Tailwind CSS, JQuery
- **Deployment:** Docker, GitHub Actions

## Production Setup

**Docker** is the only recommended way to run **pay2live** in production.  
Run the following command in a machine with Docker installed, and navigate to [localhost:5000](http://localhost:5000).

```sh
docker run \
    --name pay2live \
    --restart unless-stopped \
    -p 5000:5000 \
    -e DEBUG="False" \
    -e WHATSAPP_API_URL="https://whatsapp.tkkr.dev" \
    -e WHATSAPP_API_AUTH="YOUR_AUTH_KEY" \
    -e MONGODB_CONNECTION_URL="YOUR_DATABASE_URL" \
    -e SMTP_HOST="YOUR_SMTP_HOST" \
    -e SMTP_PORT="587" \
    -e SMTP_USERNAME="YOUR_USERNAME" \
    -e SMTP_PASSWORD="YOUR_PASSWORD" \
    -e SMTP_SENDER="YOUR_EMAIL" \
    ghcr.io/thaddeuskkr/pay2live:main
```

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

### Run the development server(s)

_Do these in separate terminals, as they are blocking processes._

#### Run Tailwind CSS (watch mode)

```sh
npm run watch
```

#### Run the Flask application

```sh
uv run flask run
```

## School Submission References

* *This project was presented at commit [`f82c7be`](https://github.com/thaddeuskkr/pay2live/commit/f82c7be87ca9b65be31fea62f105beae3d251b5d).*
* *The POLITEMall submission was made at commit [`055147d`](https://github.com/thaddeuskkr/pay2live/commit/055147d4e870818c9f8903b31991085daa2cccd8).*

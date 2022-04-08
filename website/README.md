# Airnominal Website

## About

Our website is written in [TypeScript](https://www.typescriptlang.org/) using [Vue](https://vuejs.org/) and [Vuetify](https://vuetifyjs.com/) frameworks. Charts are displayed using [Chart.js](https://www.chartjs.org/) and the map uses [Leaflet.js](https://leafletjs.com/).

## Installation

The Airnominal website requires Node.js and [Yarn](https://yarnpkg.com/) dependency manager.

You can then clone this repository and install dependencies:

```bash
git clone https://github.com/ChristofferNorgaard/Airnominal.git
cd Airnominal/website
yarn
```

## Usage

### Configuration

Airnominal uses `.env` file for configuration. Example file can be found at [`.env.sample`](.env.sample). The official API server only allows requests from the official website, so you will also have to set up your own API server.

You can also set configuration using your environment variables or in one of `.env` files [supported by Vue CLI](https://cli.vuejs.org/guide/mode-and-env.html).

### Development server

Development server can be started using:

```bash
yarn serve
```

This will automatically build the website and start the server. It includes automatic hot reloading, code linting and support for single page apps.

### Building for production

Website can be built for production using:

```bash
yarn build
```

It will build whole website, optimized for production and save it into `dist` directory. This will also include all assets and service worker file.

### Hosting for production

The website uses Vue Router in `history` mode, so a simple static file server will fail. You will need to configure your web server to fall back to the `index.html` for any non-file requests.

See [Vue Documentation](https://cli.vuejs.org/guide/deployment.html) for more details.

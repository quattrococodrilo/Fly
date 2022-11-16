# Django-Vite-Tailwind-Docker

This implementation allows you develop a Django Web App with auto reload powered by Vite.

## Install

Clone this repo and:

`./fly build`
`./fly up`

## Fly Manager

Fly is inspired in Laravel Sail, so, with this app manager you can:

- `./fly build`: Build image project.
- `./fly up`: Start services.
- `./fly down`: Shutdown services.
- `./fly --help`: Show help.
- `./fly manage`: Execute a Django command. All applications created with **startapp** will moved to apps directory.
- `./fly {npm, pnx} {command}`: Execute npm or npx command.
- `./fly mysql`: Go to MySQL cli.
- `./fly exec {django, node, mysql, exec} {command}`: Execute a command in a container.

## TODO

1. [ ] Change fly manger from Bash to Python.
2. [ ] Better documentation for **fly** manager.
3. [ ] Finish help menú.
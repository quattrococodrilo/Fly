#!/usr/bin/env python3

import argparse
import pathlib
import platform
import shlex
import shutil
import subprocess
import time
from os import getenv
from typing import Any, Dict, List

import requests
from colorama import Fore, Style
from dotenv import load_dotenv

from core.testing import dd


class EnvData:
    """Load environment variables data."""

    APPS_DIR: str = "./apps"

    APP_URL: str = "https://github.com/quattrococodrilo/Django-Vite-Tailwind-Docker/archive/refs/heads/main.zip"

    DOCKER_PROD: str = "docker-compose.yml"
    DOCKER_DEV: str = "docker-compose.yml"

    DOCKER_COMPOSE: str = "docker compose"

    def __init__(self) -> None:
        load_dotenv()

        self.APPS_DIR = getenv("APPS_DIR", "./apps")
        self.DJANGO_APP_PORT = getenv("DJANGO_APP_PORT", "80")
        self.DJANGO_APP_SERVICE = getenv("APP_SERVICE", "web")
        self.NODE_APP_SERVICE = getenv("APP_SERVICE", "node")
        self.DB_PORT = getenv("DB_PORT", "3306")
        self.WWWUSER = getenv("USERID", "1000")
        self.WWWGROUP = getenv("GROUPID", "1000")
        self.FLY_FILES = getenv("FLY_FILES")
        self.DB_APP_SERVICE = getenv("DB_HOST", "db")
        self.DB_NAME = getenv("DB_NAME", "postgres")
        self.DB_USERNAME = getenv("DB_USERNAME", "postgres")
        self.DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
        self.DB_HOST = getenv("DB_HOST", "db")
        self.DB_PORT = getenv("DB_PORT", "5432")


class Printer:
    """Handle print."""

    def printer(self, text: str, color: str = "white", style: str = "normal"):
        """Print text with color and style"""
        print(getattr(Fore, color.upper()) + getattr(Style, style.upper()) + text)

    def line(self, text: str):
        self.printer(text)

    def error(self, text: str):
        self.printer(text, color="red", style="bright")

    def warning(self, text: str):
        self.printer(text, color="yellow", style="bright")

    def success(self, text: str):
        self.printer(text, color="green", style="bright")

    def info(self, text: str):
        self.printer(text, color="blue", style="bright")


class BaseCommand:
    """Base command class."""

    ENV: EnvData = EnvData()

    subparser_dest: str
    command_name: str
    command_help: str

    printer: Printer = Printer()

    def command(self, args):
        """Define your command here."""
        pass

    def set_main_parser(self, subparsers):
        """Set main parser."""
        self.subparsers = subparsers
        return self

    def add_parser(self, subparsers):
        """Add parser to subparsers."""
        parser = subparsers.add_parser(self.command_name, help=self.command_help)
        parser.add_argument("args", nargs=argparse.REMAINDER)
        parser.set_defaults(func=self.command)

    def run_command(
        self,
        command: str,
        extra_args: List[str] = [],
        stdout_null: bool = False,
        stderr_null: bool = False,
        stdout: bool = False,
        stderr: bool = False,
    ) -> subprocess.CompletedProcess:
        """Runs command."""

        _command: List[str] = shlex.split(command)

        kwargs: Dict[str, Any] = {}

        if len(extra_args):
            _command = _command + extra_args

        if stdout_null and not stdout:
            kwargs["stdout"] = subprocess.DEVNULL
        elif not stdout_null and stdout:
            kwargs["stdout"] = subprocess.PIPE

        if stderr_null and not stderr:
            kwargs["stderr"] = subprocess.DEVNULL
        elif not stderr_null and stderr:
            kwargs["stderr"] = subprocess.PIPE

        return subprocess.run(_command, **kwargs)

    def check_docker(
        self,
        validate_file=True,
        validate_docker=True,
        validate_docker_compose=True,
        validate_fly=True,
    ):
        """Check if all related with docker is ok to run some commands."""

        if not self.docker_compose_file_exists() and validate_file:
            self.printer.error("Missing docker compose file.")
            exit(1)

        if not self.docker_is_installed() and validate_docker:
            self.printer.error("Missing docker.")
            exit(1)

        if not self.docker_compose_is_installed() and validate_docker_compose:
            self.printer.error("Missing docker compose.")
            exit(1)

        if not self.fly_is_running() and validate_fly:
            self.printer.warning("Fly is not running.")
            exit(1)

    def docker_compose_file_exists(self):
        """Check if docker compose file exists."""

        if pathlib.Path(self.ENV.DOCKER_PROD).exists():
            return True
        if pathlib.Path(self.ENV.DOCKER_DEV).exists():
            return True
        return False

    def docker_is_installed(self):
        """Check if docker is installed."""

        try:
            completed_process = self.run_command(
                "docker info",
                stdout_null=True,
                stderr=True,
            )
        except FileNotFoundError:
            return False

        if completed_process.returncode == 0:
            return True
        return False

    def docker_compose_is_installed(self):
        """Check if docker compose is installed."""

        try:
            completed_process = self.run_command(
                "docker compose",
                stdout_null=True,
                stderr=True,
            )
            self.ENV.DOCKER_COMPOSE = "docker compose"
        except FileNotFoundError:
            try:
                completed_process = self.run_command(
                    "docker-compose",
                    stdout_null=True,
                    stderr=True,
                )
                self.ENV.DOCKER_COMPOSE = "docker-compose"
            except FileNotFoundError:
                return False

        if completed_process.returncode == 0:
            return True
        return False

    def fly_is_running(self):
        """Check if Fly is running."""

        completed_process = self.run_command(
            f"docker compose ps {self.ENV.DJANGO_APP_SERVICE}",
            stdout_null=True,
            stderr=True,
        )

        if completed_process.returncode == 0:
            return True
        return False


class Fly:
    """
    Fly commands.
    """

    ENV: EnvData = EnvData()

    commands: List[Dict[str, Any]] = []

    printer: Printer = Printer()

    def __init__(self):
        self._system = self.uname_s()

        if self._system != "Linux" and self._system != "Darwin":
            self.printer.error("System not supported")
            raise ValueError("System not supported")

        self.parser = argparse.ArgumentParser(
            description="Fly is a command line tool for managing your Django projects."
        )
        self.subparsers = self.parser.add_subparsers()
        self.start_parser()

    @classmethod
    def run(cls):
        """Run Fly."""

        return cls()

    def command_register(self):
        """Commands register."""

        return [
            InstallFlyCommand().set_main_parser(self.subparsers),
            UpServicesCommand().set_main_parser(self.subparsers),
            DownServicesCommand().set_main_parser(self.subparsers),
            DockerComposeCommand().set_main_parser(self.subparsers),
            PipCommand().set_main_parser(self.subparsers),
            DjangoManageCommand().set_main_parser(self.subparsers),
            NpmCommand().set_main_parser(self.subparsers),
            MySqlCommand().set_main_parser(self.subparsers),
            PostgreSqlCommand().set_main_parser(self.subparsers),
        ]

    def start_parser(self):
        """Start the parser."""

        self.register()
        args = self.parser.parse_args()
        if "func" in args:
            args.func(args)
        else:
            self.parser.print_help()

    def register(self):
        """Register parser in subparsers."""

        for command in self.command_register():
            command.add_parser(self.subparsers)

    def uname_s(self):
        """Check OS type."""

        info = platform.uname()
        return info.system


class InstallFlyCommand(BaseCommand):
    """Installs app."""

    subparser_dest: str = "Install"
    command_name: str = "install"
    command_help: str = "Install app."

    def command(self, args):
        python_packages = shlex.split("pip install colorama requests python-dotenv")
        subprocess.run(python_packages)

        self.printer.success("Basic install, done...")
        self.printer.info("Installing app..")

        zip_file = pathlib.Path("django_fly.zip")
        project_dir = pathlib.Path("Django-Vite-Tailwind-Docker-main")

        response = requests.get(self.ENV.APP_URL)
        zip_file.write_bytes(response.content)

        # result = subprocess.run(shlex.split(f"unzip {zip_file} -d ."))
        result = self.run_command(f"unzip {zip_file} -d .")
        if result.returncode != 0:
            print(f"Error al descomprimir {zip_file}")
            return

        if zip_file.exists():
            zip_file.unlink()

        if project_dir.exists():
            for file in project_dir.iterdir():
                shutil.move(file, ".")

            shutil.rmtree(project_dir)


class UpServicesCommand(BaseCommand):
    """Up services."""

    subparser_dest: str = "Up"
    command_name: str = "up"
    command_help: str = "Up services."

    def command(self, args):
        self.check_docker(validate_fly=False)
        try:
            self.printer.info("Shuting down old services...")
            self.run_command(
                "docker rm -f $(docker ps -aq)",
                stdout_null=True,
                stderr_null=True,
            )
            self.run_command(
                f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} up",
                extra_args=args.args,
            )
        except KeyboardInterrupt:
            self.printer.info("Services removed.")


class DownServicesCommand(BaseCommand):
    """Down services."""

    subparser_dest: str = "Down"
    command_name: str = "down"
    command_help: str = "Down services."

    def command(self, args):
        self.check_docker()
        try:
            self.run_command(
                f"docker compose -f {self.ENV.DOCKER_DEV} down",
                extra_args=args.args,
            )
            self.run_command(
                "docker rm -f $(docker ps -aq)",
                stdout_null=True,
                stderr_null=True,
            )
        except KeyboardInterrupt:
            self.printer.info("Services removed.")


class DockerComposeCommand(BaseCommand):
    """Execute docker compose commands."""

    subparser_dest: str = "docker_compose"
    command_name: str = "dc"
    command_help: str = "Exec docker compose commands."

    def command(self, args):
        self.check_docker()
        self.run_command(
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV}", extra_args=args.args
        )


class PipCommand(BaseCommand):
    """Execute pip commands."""

    subparser_dest: str = "pip"
    command_name: str = "pip"
    command_help: str = "Execute pip commands"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec -u fly"
            f" {self.ENV.DJANGO_APP_SERVICE} venv/bin/pip"
        )
        self.run_command(cmd, extra_args=args.args)


class DjangoManageCommand(BaseCommand):
    """Execute manage.py commands."""

    subparser_dest: str = "manage"
    command_name: str = "manage"
    command_help: str = "Execute Django Manager"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec -u fly "
            f" {self.ENV.DJANGO_APP_SERVICE} venv/bin/python manage.py"
        )
        self.run_command(cmd, extra_args=args.args)

        if "startapp" in args.args:
            shutil.move(args.args[-1], self.ENV.APPS_DIR)


class NpmCommand(BaseCommand):
    """Execute NPM commands."""

    subparser_dest: str = "npm"
    command_name: str = "npm"
    command_help: str = "Execute npm"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec -u fly"
            f" {self.ENV.NODE_APP_SERVICE} npm"
        )
        self.run_command(cmd, extra_args=args.args)


class NpxCommand(BaseCommand):
    """Execute NPX commands."""

    subparser_dest: str = "npx"
    command_name: str = "npx"
    command_help: str = "Execute npx"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec -u fly"
            f" {self.ENV.NODE_APP_SERVICE} npx"
        )
        self.run_command(cmd, extra_args=args.args)


class MySqlCommand(BaseCommand):
    """Execute MySql commands."""

    subparser_dest: str = "mysql"
    command_name: str = "mysql"
    command_help: str = "Execute MySql"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec db bash -c"
            f' "MYSQL_PWD={self.ENV.DB_PASSWORD}'
            f' mysql -u {self.ENV.DB_USERNAME} {self.ENV.DB_NAME}"'
        )
        self.run_command(cmd, extra_args=args.args)


class PostgreSqlCommand(BaseCommand):
    """Execute PostgreSQL commands."""

    subparser_dest: str = "psql"
    command_name: str = "psql"
    command_help: str = "Execute PostgreSQL"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV}"
            f" exec {self.ENV.DB_APP_SERVICE} bash -c"
            f' "PGPASSWORD={self.ENV.DB_PASSWORD}'
            f' psql -U {self.ENV.DB_USERNAME} {self.ENV.DB_NAME}"'
        )
        self.run_command(cmd, extra_args=args.args)


if __name__ == "__main__":
    Fly.run()

"""
Testing script that runs all the tests and handles the Docker containers as well as the tests.
"""

import os
import time
import unittest

import docker

TEST_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
ROOT_DIR = os.path.join(TEST_DIR, "..")
os.environ["PYTHONPATH"] = ROOT_DIR
DOCKER_CLIENT = docker.from_env()


class DbInstance:
    """
    Handles the Docker container for the surrpy.

    Attributes:
        version (str): The version of the surrpy to run.
        port (int): The port to run the surrpy on.
        container (docker.models.containers.Container): The Docker container instance.
        id (str): The id of the Docker container.
    """

    def __init__(self, version: str, port: int = 8000) -> None:
        """
        The constructor for the DbInstance class.

        :param version: The version of the surrpy to run.
        :param port: The port to run the surrpy on.
        """
        self.version: str = version
        self.port: int = port
        self.container = None
        self.id = None

    def start(self) -> None:
        """
        Starts the Docker container.

        :return: None
        """
        self.container = DOCKER_CLIENT.containers.run(
            image=f"surrpy/surrpy:{self.version}",
            command="start",
            environment={
                "SURREAL_USER": "root",
                "SURREAL_PASS": "root",
                "SURREAL_LOG": "trace",
            },
            ports={"8000/tcp": self.port},
            detach=True,
        )
        self.id = self.container.id

    def stop(self) -> None:
        """
        Stops the Docker container.

        :return: None
        """
        self.container.stop()

    def remove(self) -> None:
        """
        Removes the Docker container.

        :return: None
        """
        self.container.remove()


def run_tests(port: int, protocol: str) -> None:
    os.environ["CONNECTION_PROTOCOL"] = f"{protocol}"
    os.environ["CONNECTION_PORT"] = f"{port}"
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir=TEST_DIR, pattern="test*.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    _ = test_runner.run(test_suite)


if __name__ == "__main__":
    port = 8000
    for version in [
        "v2.0.2",
    ]:
        container = DbInstance(version=version, port=port)
        container.start()
        time.sleep(0.3)
        print(f"Running tests for version {version} on port {container.port}")
        run_tests(port=container.port, protocol="http")
        run_tests(port=container.port, protocol="ws")
        container.stop()
        container.remove()
        port += 1

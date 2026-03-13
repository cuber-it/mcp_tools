"""Pure tool logic for docker — no MCP dependency."""

from __future__ import annotations

from .client import DockerClient

def container_list(client: DockerClient, all: bool = False) -> str:
    """List containers"""
    # TODO: implement
    raise NotImplementedError("container_list")


def container_start(client: DockerClient, container_id: str) -> str:
    """Start a stopped container"""
    # TODO: implement
    raise NotImplementedError("container_start")


def container_stop(client: DockerClient, container_id: str, timeout: int = 10) -> str:
    """Stop a running container"""
    # TODO: implement
    raise NotImplementedError("container_stop")


def container_restart(client: DockerClient, container_id: str) -> str:
    """Restart a container"""
    # TODO: implement
    raise NotImplementedError("container_restart")


def container_remove(client: DockerClient, container_id: str, force: bool = False) -> str:
    """Remove a container"""
    # TODO: implement
    raise NotImplementedError("container_remove")


def container_logs(client: DockerClient, container_id: str, tail: int = 100) -> str:
    """Get container logs"""
    # TODO: implement
    raise NotImplementedError("container_logs")


def container_inspect(client: DockerClient, container_id: str) -> str:
    """Inspect container details"""
    # TODO: implement
    raise NotImplementedError("container_inspect")


def image_list(client: DockerClient) -> str:
    """List local images"""
    # TODO: implement
    raise NotImplementedError("image_list")


def image_pull(client: DockerClient, image: str) -> str:
    """Pull an image from registry"""
    # TODO: implement
    raise NotImplementedError("image_pull")


def image_remove(client: DockerClient, image: str, force: bool = False) -> str:
    """Remove a local image"""
    # TODO: implement
    raise NotImplementedError("image_remove")


def volume_list(client: DockerClient) -> str:
    """List volumes"""
    # TODO: implement
    raise NotImplementedError("volume_list")


def network_list(client: DockerClient) -> str:
    """List networks"""
    # TODO: implement
    raise NotImplementedError("network_list")


def compose_up(client: DockerClient, path: str, detach: bool = True) -> str:
    """Start services from compose file"""
    # TODO: implement
    raise NotImplementedError("compose_up")


def compose_down(client: DockerClient, path: str) -> str:
    """Stop and remove compose services"""
    # TODO: implement
    raise NotImplementedError("compose_down")


def compose_ps(client: DockerClient, path: str) -> str:
    """List compose service status"""
    # TODO: implement
    raise NotImplementedError("compose_ps")


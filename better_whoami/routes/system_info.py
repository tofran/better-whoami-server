import os
import platform
import socket
import sys
from dataclasses import dataclass
from typing import Any

import psutil
from litestar import get


@dataclass
class ProcessInfo:
    pid: int
    name: str
    ppid: int
    cpu_utilization: float
    memory_usage: dict[str, int]


@dataclass
class MemoryInfo:
    total_bytes: int
    available_bytes: int
    percent: float
    used_bytes: int


@dataclass
class CpuInfo:
    physical_cores_count: int | None
    total_cores_count: int | None
    utilization: float
    cpu_frequency: dict[str, Any] | None


@dataclass
class Partition:
    device: str
    mountpoint: str
    fstype: str
    opts: str


@dataclass
class DiskInfo:
    usage: dict[str, int]
    partitions: list[Partition]


@dataclass
class SystemInfo:
    hostname: str
    fqdn: str
    platform: str
    python_version: str
    process: ProcessInfo
    memory: MemoryInfo
    cpu: CpuInfo
    disk: DiskInfo


@get(
    "/system_info",
    name="system_info",
    description="Get system information, like disk usage, memory, cpu, etc.",
    sync_to_thread=False,
)
def system_info() -> SystemInfo:
    process_info = ProcessInfo(
        pid=os.getpid(),
        ppid=os.getppid(),
        name=psutil.Process().name(),
        cpu_utilization=psutil.Process().cpu_percent(),
        memory_usage=psutil.Process().memory_info()._asdict(),
    )

    memory = psutil.virtual_memory()
    memory_info = MemoryInfo(
        total_bytes=memory.total,
        available_bytes=memory.available,
        used_bytes=memory.used,
        percent=memory.percent,
    )

    cpu_info = CpuInfo(
        physical_cores_count=psutil.cpu_count(logical=False),
        total_cores_count=psutil.cpu_count(logical=True),
        cpu_frequency=psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        utilization=psutil.cpu_percent(interval=1),
    )

    disk_info = DiskInfo(
        usage={
            f"{key}_bytes": value  # fmt: skip
            for key, value in psutil.disk_usage("/")._asdict().items()
        },
        partitions=[
            Partition(
                device=partition.device,
                mountpoint=partition.mountpoint,
                fstype=partition.fstype,
                opts=partition.opts,
            )
            for partition in psutil.disk_partitions()
        ],
    )

    return SystemInfo(
        hostname=socket.gethostname(),
        fqdn=socket.getfqdn(),
        platform=platform.platform(),
        python_version=sys.version,
        process=process_info,
        memory=memory_info,
        cpu=cpu_info,
        disk=disk_info,
    )

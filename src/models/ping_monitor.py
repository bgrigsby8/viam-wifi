import subprocess
import time
from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence)

from typing_extensions import Self
from viam.components.sensor import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes, struct_to_dict


def check_ping(host):
    try:
        result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
        if "time=" in result.stdout:
            ping_time = float(result.stdout.split("time=")[1].split(" ms")[0])
            return ping_time
        return None
    except Exception:
        return None

class PingMonitor(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(ModelFamily("brad-grigsby", "wifi"), "ping-monitor")

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        attributes = struct_to_dict(config.attributes)

        if "router_address" not in attributes:
            raise Exception("router_address is required")
        elif not isinstance(attributes["router_address"], str):
            raise Exception("router_address must be a string")
        
        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        attributes = struct_to_dict(config.attributes)

        self.router_address = attributes["router_address"]

        return super().reconfigure(config, dependencies)

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        # Check connectivity to the router (Local Network)
        router_ping = check_ping(self.router_address)

        # Check connectivity to the internet
        internet_ping = check_ping("8.8.8.8")

        return {
            "router_ping": router_ping,
            "internet_ping": internet_ping,
        }


    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        raise NotImplementedError()


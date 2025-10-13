"""
Connector factory for sync operations.
"""

from typing import Dict, Any


def get_connector(config: Dict[str, Any]):
    """
    Get connector instance for calendar config.

    Args:
        config: Calendar configuration dict with type and credentials

    Returns:
        Connector instance

    Raises:
        NotImplementedError: If connector type not supported
    """
    if config['type'] == 'graph':
        from ...connectors import GraphConnector
        return GraphConnector(config['credentials'])
    elif config['type'] == 'google':
        from ...connectors import GoogleConnector
        return GoogleConnector(config['credentials'])
    elif config['type'] == 'icloud':
        from ...connectors.icloud_connector import ICloudConnector
        return ICloudConnector(config['credentials'])
    else:
        raise NotImplementedError(
            f"Connector type {config['type']} not implemented"
        )

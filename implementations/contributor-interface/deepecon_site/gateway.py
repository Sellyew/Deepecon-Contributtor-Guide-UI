"""The model gateway (plan §1; D-042).

The contributor site sends nothing to AI services. This module is the only place where a
model call could ever be made, and in v1 it refuses every call. An AI feature can be added
later only through this module and only if the research lead configures it; it would never
receive restricted data, and contributors' material only with their recorded consent.
A test checks that no other module opens a network connection.
"""


class ModelGatewayDisabled(RuntimeError):
    """Raised for every call: v1 has no model integration."""


def call_model(*args, **kwargs):
    raise ModelGatewayDisabled(
        "The model gateway refuses every call in v1: the contributor site sends nothing to AI services (D-042)."
    )

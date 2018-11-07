Publisher
=========
The Publisher block sends input signals to the configured topic. Publisher blocks can send signals on a configured topic to any instance within the same system. Signals must be valid JSON.

Properties
----------
- **topic**: Hierarchical topic string to publish to.

Inputs
------
- **default**: Each input signal will be sent along to the appropriate Subscribers based on the *topic*.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
None
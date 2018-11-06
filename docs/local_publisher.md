LocalPublisher
==============
The LocalPublisher publishes incoming signals to the configured topic. Topics can be static or dynamic bassed on the first signal in a list of signals. Only LocalSubscriber blocks on the same nio instance can subscribe to this data. Unlike the regular [Publisher block](https://blocks.n.io/Publisher), these signals do not need to contain data that is valid JSON.

Properties
----------
- **local_identifier**: Hidden property with a default of `[[INSTANCE_ID]]`. Unique identifier of this instance in the nio system.
- **topic**: Hierarchical topic string to publish to.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
None
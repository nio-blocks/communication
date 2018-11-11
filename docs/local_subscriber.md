LocalSubscriber
===============
The LocalSubscriber block subscribes to the configured topic and outputs signals received. Only LocalPublisher blocks on the same nio instance can send data to the LocalSubscriber blocks. Unlike the Subscriber block, these signals do not need to contain data that is valid JSON.

Properties
----------
- **local_identifier**: Hidden property with a default of `[[INSTANCE_ID]]`. Unique identifier of this instance in the nio system.
- **topic**: Hierarchical topic string to subscribe to.

Inputs
------
None

Outputs
-------
- **default**: A signal of the message published to the configured topic.

Commands
--------
None

Dependencies
------------
None
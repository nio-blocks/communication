LocalPublisher
==============
The LocalPublisher publishes incoming signals to the configured topic. Topics can be static or dynamic bassed on the first signal in a list of signals. Only LocalSubscriber blocks on the same nio instance can subscribe to this data. Unlike the regular [Publisher block](https://blocks.n.io/Publisher), these signals do not need to contain data that is valid JSON.

Properties
----------
- **local_identifier**: Hidden property with a default of `[[INSTANCE_ID]]. Unique identifier of this instance in the nio system.
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

***

LocalSubscriber
===============
The LocalSubscriber block subscribes to the configured topic and outputs signals received. Only LocalPublisher blocks on the same nio instance can send data to the block. Unlike the regular [Subscriber block](https://blocks.n.io/Subscriber), these signals do not need to contain data that is valid JSON.

Properties
----------
- **local_identifier**: Hidden property with a default of `[[INSTANCE_ID]]. Unique identifier of this instance in the nio system.
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

***

Publisher
=========
The Publisher block sends incoming signals to the configured topic. Topics can be static or dynamic bassed on the first signal in a list of signals.

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

***

Subscriber
==========
The Subscriber block reads data from the configured topic and output signals received.

Properties
----------
- **topic**: Hierarchical topic string to subscribe to.

Inputs
------
None

Outputs
-------
- **default**: Signal list for each message received on topic.

Commands
--------
None

Dependencies
------------
None


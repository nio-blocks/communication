LocalPublisher
==============
The LocalPublisher publishes incoming signals to the configured topic. Only LocalSubscriber blocks on the same nio instance can subscribe to this data. Signals will be pickled before publishing, so unlike the "regular" Publisher the entire signal does not need to be JSON-serializable.

Properties
----------
- **local_identifier**: Hidden property with a default of `[[INSTANCE_ID]]`, the unique identifier of this instance in the nio system.
- **timeout**: If a connection cannot be made in this time the block will be put into `warning` status.
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
The LocalSubscriber block subscribes to the configured topic and outputs signals received. Only LocalPublisher blocks on the same nio instance can send data to the block.

Properties
----------
- **local_identifier**: Hidden property with a default of `[[INSTANCE_ID]]`, the unique identifier of this instance in the nio system.
- **timeout**: If a connection cannot be made in this time the block will be put into `warning` status.
- **topic**: Hierarchical topic string to subscribe to, supports `*` as a wildcard character.

Inputs
------
None

Outputs
-------
- **default**: The same list of signals that was published to the configured `topic` by a LocalPublisher.

Commands
--------
None

Dependencies
------------
None

***

Publisher
=========
The Publisher block sends incoming signals to the configured topic. The entire signal must be JSON-serializable. For signals that cannot be represented in JSON, use a LocalPublisher if appropriate or [Pickle](https://github.com/nio-blocks/pickle) signals before publishing.

Properties
----------
- **timeout**: If a connection cannot be made in this time the block will be put into `warning` status.
- **topic**: Hierarchical topic string to publish to.

Inputs
------
- **default**: Any list of signals that can be serialized into JSON.

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
- **timeout**: If a connection cannot be made in this time the block will be put into `warning` status.
- **topic**: Hierarchical topic string to subscribe to, supports `*` as a wildcard character.

Inputs
------
None

Outputs
-------
- **default**: The same list of signals that was published to the configured `topic` by a Publisher.

Commands
--------
None

Dependencies
------------
None


LocalPublisher
==============
Publish input signals to the configured topic. Only LocalSubscriber blocks on the same nio instance can subscribe to this data. Unlike the regular Publisher block, these signals do not need to contain data this is valid JSON.

Properties
----------
- **local_identifier**: Unique identifier of this instance in the nio system.
- **topic**: Hierarchical topic string to publish to

Inputs
------
- **default**: 

Outputs
-------

Commands
--------

***

LocalSubscriber
===============
Subscribe to the configured topic and output signals received. Only LocalSubscriber blocks on the same nio instance can subscribe to this data. Unlike the regular Publisher block, these signals do not need to contain data this is valid JSON.

Properties
----------
- **local_identifier**: Unique identifier of this instance in the nio system.
- **topic**: Hierarchical topic string to publish to

Inputs
------

Outputs
-------
- **default**: 

Commands
--------

***

Publisher
=========
Publish input signals to the configured topic

Properties
----------
- **topic**: Hierarchical topic string to publish to

Inputs
------
- **default**: Publish each list of signals

Outputs
-------

Commands
--------

Dependencies
------------
None

Input
-----
Each input signal will be sent along to the appropriate Subscribers based on the *topic*.

Output
------
None

***

Subscriber
==========
Subscribe to the configured topic and output signals received

Properties
----------
- **topic**: Hierarchical topic string to subscribe to

Inputs
------

Outputs
-------
- **default**: Signal list for each message received on topic

Commands
--------

Dependencies
------------
None

Input
-----
None

Output
------
An output signal is created when the appropriate Publishers send signals based on the *topic*.


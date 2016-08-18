Communication
=======

Publisher and Subscriber blocks to send signals between Services and nio Instances.

-   [Publisher](https://github.com/nio-blocks/communication#publisher)
-   [Subscriber](https://github.com/nio-blocks/communication#subscriber)

***

Publisher
===========

Input signals will be sent to the appropriate Subscribers based on the *topic*.

Properties
--------------

-   **topic**: Defines topic string to use to publish signals.


Dependencies
----------------
None

Commands
----------------
None

Input
-------
Each input signal will be sent along to the appropriate Subscribers based on the *topic*.

Output
---------
None

***

Subscriber
===========

Output signals will be created when the appropriate Publishers send signals based on the *topic*.

Properties
--------------

-   **topic**: Defines topic string to subscribe to in order to receive signals.

Dependencies
----------------
None

Commands
----------------
None

Input
-------
None

Output
---------
An output signal is created when the appropriate Publishers send signals based on the *topic*.

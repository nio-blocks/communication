Communication
=======

Publisher and Subscriber blocks to send signals between Services and nio Instances.

-   [Publisher](https://github.com/nio-blocks/communication#publisher)
-   [Subscriber](https://github.com/nio-blocks/communication#subscriber)

***

Publisher
===========

Input signals will be sent to the appropriate Subscribers based on the *criteria*.

Properties
--------------

-   **criteria**: Criteria to determine where to send signals.
  -   **keyword**: (str) Key to subscribe to. Will send to all subscribers with this key that meet the **rules**
  -   **rules**: (str, Called FilterValues): Rules that must be met by subscriber. If you have rule {KEY: [A, B]} then subscribers that have keyword=KEY and rules [], [A] or [A, B] will receieve the signal. If a rule is wrong, i.e. [A, C] then it will not receive the signal.


Dependencies
----------------
None

Commands
----------------
None

Input
-------
Each input signal will be sent along to the appropriate Subscribers based on the *criteria*.

Output
---------
None

***

Subscriber
===========

Output signals will be created when the appropriate Publishers send signals based on the *criteria*.

Properties
--------------

-   **criteria**: Criteria to determine what signals to receive.
  -   **keyword**: See Publisher
  -   **rules**: See Publisher

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
An output signal is created when the appropriate Publishers send signals based on the *criteria*.

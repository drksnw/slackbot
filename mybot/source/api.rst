Explore API
***********

This file describes functions used by the bot.

Weather API Functions
====================

.. py:function:: get_weather(city[, country='ch'])

   Gets the actual weather from OpenWeatherMap API for the specified *city*.

Slack API Functions
==================

.. py:function:: send_message(chan, txt)

   Sends a message to the specific channel.

.. py:function:: consumer(message)

   Method is called when the bot gets a *message*.
   This function parses the *message* and does something.

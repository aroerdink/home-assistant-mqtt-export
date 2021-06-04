"""
MQTT publisher for all Home Assistant states.

Copyright (c) 2016 Fabian Affolter <fabian@affolter-engineering.ch>
Licensed under MIT

For questions and issues please use https://community.home-assistant.io

To use this component you will need to add something like the
following to your configuration.yaml file.

mqtt_export:
  publish_topic: "home-assistant/states"
"""
import logging

import homeassistant.loader as loader
from homeassistant.components import mqtt
from homeassistant.const import (STATE_UNKNOWN, EVENT_STATE_CHANGED)
from homeassistant.helpers.json import JSONEncoder

DOMAIN = "mqtt_export"
DEPENDENCIES = ['mqtt']

DEFAULT_TOPIC = 'home-assistant/states'
PAYLOAD = None

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Setup the MQTT export component."""
    _LOGGER.warning('MQTT export started')
    pub_topic = config[DOMAIN].get('publish_topic', DEFAULT_TOPIC)

    global PAYLOAD
    PAYLOAD = dict(states=None, details=None)

    # Add the configuration
    PAYLOAD['details'] = hass.config.as_dict()

    def mqtt_event_listener(event):
        """Listen for new messages on the bus and send data to MQTT."""
        state = event.data.get('new_state')
        if state is None or state.state in (STATE_UNKNOWN, ''):
            return None

        """Create topic from entity_id."""
        topic = "%s/%s" % (pub_topic, event.data.get('entity_id'))
        _LOGGER.debug('Publishing "%s" to "%s"', state.state, topic)

        mqtt.publish(hass, topic, state.state)

    hass.bus.listen(EVENT_STATE_CHANGED, mqtt_event_listener)

    return True

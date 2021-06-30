#!/usr/bin/env python3
"""
A little script that I wrote to demonstrate how to address a problem by decomposing it into classes.

The original question I was answering was something along the lines of how to deal with configuration after requesting it from a user on https://github.com/absenth/agridies

It seemed like a good opportunity to write a small demonstration of some gotchas and things to think about.
"""

from collections import defaultdict
import os
from pprint import pprint
from typing import Optional, Tuple

RUN_DEMOS = False

class Config:
    def __init__(self, category:str, callsign: str, station: str ):
        self._category = category
        self._callsign = callsign
        self._station = station

    def __repr__(self):
        return f"{self.category}/{self.station}/{self.callsign}"

    @property
    def category(self):
        return self._category

    @property
    def callsign(self):
        return self._callsign

    @callsign.setter
    def callsign(self, value: str):
        print(f'Updating station {self.station} from {self.callsign} to {value}')
        self._callsign = value

    @property
    def station(self):
        return self._station

    @classmethod
    def from_input(cls) -> 'Config':
        category = input("category> ")
        callsign = input("callsign> ")
        station = input("station> ")
        return cls(category, callsign, station)
    
    @classmethod
    def from_env(cls) -> 'Config':
        category = os.environ["APP_CATEGORY"]
        callsign = os.environ["APP_CALLSIGN"]
        station = os.environ["APP_STATION"]
        return cls(category, callsign, station)

    @staticmethod
    def format_something(category: str):
        print(f"formatting {category}")
        return category.upper()

class Config2:
    """
    Just for demonstrating downsides of mutable values
    """
    def __init__(self, category:str, callsign: str, station: str ):
        self.category = category
        self.callsign = callsign
        self.station = station
    def __repr__(self):
        return f"{self.category}/{self.callsign}/{self.station}"

def setup_function(callsign, station):
    """
    Just for demonstrating downsides of mutable values
    """
    category = input('category> ')
    return {
        "category": category,
        "callsign": callsign,
        "station": station,
    }

class App:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._last_callsign = cfg.callsign
        self.contacts = defaultdict(list)

    @property
    def last_callsign(self):
        return self._last_callsign

    @last_callsign.setter
    def last_callsign(self, callsign):
        if callsign != self._last_callsign:
            print(f"Switching to {callsign} from {self._last_callsign}")
            self._last_callsign = callsign

    def log_a_contact(self, contact):
        return f"Contact with {contact} from {self.cfg.station} by {self.cfg.callsign}"

    def log_a_different_contact(self, local_callsign: str, remote_callsign: Optional[str] = None):
        if not local_callsign:
            local_callsign = self.last_callsign
        self._update_db(local_callsign, remote_callsign)
        return f"A different sort of contact with {remote_callsign} from {self.cfg.station} by {local_callsign}"

    def _update_db(self, local_station: str, remote_station: str):
        """
        Update the "database" and populate the last_callsign
        """
        self.contacts[local_station].append(remote_station)
        self.last_callsign = local_station

    def _get_input(self) -> Tuple[str,str]:
        while True:
            try:
                contact = input("Log Contact > ")
            except (KeyboardInterrupt, EOFError):
                print()
                return None
            if contact == "quit":
                return None
            if contact:
                return self._parse_input(contact)

            print("I need something that's not empty")
            
    def _parse_input(self, value) -> Tuple[str,str]:
        parts = value.split('/')
        if len(parts) == 2:
            local_callsign = parts[0]
        else:
            local_callsign = self._last_callsign
        remote_callsign = parts[-1]
        return local_callsign, remote_callsign

    def run(self):
        print('Type quit to quit')

        while True:
            res = self._get_input()
            if not res:
                break
            self.log_a_different_contact(*res)
        pprint(dict(self.contacts))

    @classmethod
    def setup(cls):
        cfg = Config.from_env()
        return cls(cfg)

def make_sure_env_setup_for_demo():
    """
    Populate some environment variables so we don't have to bother setting them
    just for a demo
    """
    if not "APP_CATEGORY" in os.environ:
        os.environ["APP_CATEGORY"] = "strange_folks"
    if not "APP_CALLSIGN" in os.environ:
        os.environ["APP_CALLSIGN"] = "ke5gqs"
    if not "APP_STATION" in os.environ:
        os.environ["APP_STATION"] = "iss"
def demos():
    # manually setting up an App and Config
    cfg_manual = Config(
        category='derby_players',
        callsign='ke5gqs',
        station='union'
    )
    app_manual = App(cfg_manual)
    
    # Using a classmethod on the Config class to create a new class instance
    cfg_from_input = Config.from_input()
    app_from_input = App(cfg_from_input)
    
    # Use a classmethod on the App class to automatically set up a config object
    make_sure_env_setup_for_demo()
    app = App.setup()
    
    # Demonstrate that our properties are read only without a setter
    # technically they're still mutable under the hood
    try:
        app.cfg.category = "folks_who_dont_know_about_properties"
    except AttributeError:
        print("Can't update it")
    # Technically you can still update them, but things prefixed with an _ are considered private 
    # Pylint will throw an error if we do this, but we technically can
    app.cfg._category = "folks_who_are_sneaky"
    
    # Demonstrate that our @property with a setter logs a message when we update the callsign
    app.log_a_contact('wwv')
    app.cfg.callsign = "w9zeb"
    app.log_a_contact('wwvb')
    

if RUN_DEMOS:
    demos()

if __name__ == "__main__":
    make_sure_env_setup_for_demo()
    app = App.setup()
    app.run()
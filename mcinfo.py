#!/usr/bin/env python3
###############################################################################
# Gathers Minecraft player name history and info. 
# Uses the Mojang API - https://wiki.vg/Mojang_API
#
# Author: PotatoMaster101
# Date:   11/02/2019
###############################################################################

import argparse
import json
import base64
import urllib.request
from datetime import datetime

def get_args():
    """
    Returns the arguments from the user. 
    """
    p = argparse.ArgumentParser(description="Minecraft player info.")
    p.add_argument("name", type=str, nargs="+", 
            help="one or more player names")
    p.add_argument("-v", "--verbose", action="store_true", dest="verbose", 
            help="display more information")
    return p


def get_json(raw):
    """
    Returns the given text expressed as JSON, or None if any error occurred. 
    """
    try:
        return json.loads(raw)
    except:
        return None


def get_site_json(url):
    """
    Performs a GET request and returns the JSON returned by the given site. 
    """
    with urllib.request.urlopen(url) as res:
        return get_json(res.read())


def get_uuid(name):
    """
    Returns the UUID of the given player name. 
    """
    url = "https://api.mojang.com/users/profiles/minecraft/%s" %name
    res = get_site_json(url)
    return res["id"] if res else None


def get_hist(name):
    """
    Returns the name history of the given player name. 
    """
    uuid = get_uuid(name)
    url = "https://api.mojang.com/user/profiles/%s/names" %uuid
    res = get_site_json(url)
    return (res, uuid) if res else (None, None)


def get_profile(name):
    """
    Returns the player profile and the base64 decoded skin info. 
    """
    uuid = get_uuid(name)
    url = "https://sessionserver.mojang.com/session/minecraft/profile/%s" %uuid
    try:
        res = get_site_json(url)    # throws HTTP error 429 if on cooldown
        skin = None
        if res:
            skin = base64.b64decode(res["properties"][0]["value"])
            skin = skin.decode("utf-8")
        return res, get_json(skin)
    except:
        return None, None   # 1 minute cooldown for same name according to API


def get_date(time):
    """
    Converts the given timestamp (in milliseconds) to a date. 
    """
    return datetime.fromtimestamp(float(time) / 1000)


def print_hist(name):
    """
    Prints username history. 
    """
    print("### Histories:")
    hist, uuid = get_hist(name)
    if not hist:
        print("Not found")
        return False

    for h in hist:
        if "changedToAt" in h:
            date = get_date(h["changedToAt"])
            print("> %-30s (since %s)" %(h["name"], date))
        else:
            print("> %-30s (original, %s)" %(h["name"], uuid))
    return True


def print_prof(name):
    """
    Prints the user profile. 
    """
    print("\n### Extras")
    res, skin = get_profile(name)
    if res and skin:
        skinurl = None
        if "SKIN" in skin["textures"]:
            skinurl = skin["textures"]["SKIN"]["url"]
        capeurl = None
        if "CAPE" in skin["textures"]:
            capeurl = skin["textures"]["CAPE"]["url"]
        print("UUID:     %s" %res["id"])
        print("Migrated: %s" %("No" if "legacy" in res else "Yes"))
        print("Skin URL: %s" %skinurl)
        print("Cape URL: %s" %capeurl)
    else:
        print("User not found or service cooldown, wait for 1 minute")


if __name__ == "__main__":
    """
    Entry point. 
    """
    argp = get_args().parse_args()
    for i, n in enumerate(argp.name):
        print("##### Username: %s" %n)
        print_hist(n)
        if argp.verbose:
            print_prof(n)
        if i != (len(argp.name) - 1):
            print("\n")


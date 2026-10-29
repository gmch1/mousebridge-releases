#!/usr/bin/env python3
"""Publish verified assets first; then advance the signed rolling feed."""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from verify import REPO, SPARKLE, verify


def gh(*arguments):
    return subprocess.check_output(["gh", *arguments, "--repo", REPO], text=True)


def releases():
    return json.loads(gh("release", "list", "--limit", "1000", "--json", "tagName,isDraft"))


def publish(directory):
    directory = pathlib.Path(directory)
    metadata, assets = verify(directory)
    tag = metadata["tag"]
    existing = next((r for r in releases() if r["tagName"] == tag), None)
    if existing:
        # Retrying may finish a draft or advance the feed, but never replace
        # the contents of an existing version with a different binary.
        with tempfile.TemporaryDirectory() as temporary:
            gh("release", "download", tag, "--dir", temporary)
            for name in assets:
                previous = pathlib.Path(temporary) / name
                if not previous.exists() or previous.read_bytes() != (directory / name).read_bytes():
                    raise ValueError("Existing release differs; use a new version: " + name)
    else:
        gh("release", "create", tag, "--draft", "--target", os.environ["GITHUB_SHA"],
           "--title", "MouseBridge " + tag, "--notes-file", str(directory / "notes.md"),
           *[str(directory / name) for name in assets])
    if not existing or existing["isDraft"]:
        options = ["--draft=false"]
        if metadata["prerelease"]:
            options += ["--prerelease", "--latest=false"]
        else:
            options += ["--prerelease=false", "--latest"]
        gh("release", "edit", tag, *options)
    if any(r["tagName"] == "appcast" for r in releases()):
        with tempfile.TemporaryDirectory() as temporary:
            gh("release", "download", "appcast", "--pattern", "appcast.xml", "--dir", temporary)
            root = ET.parse(pathlib.Path(temporary) / "appcast.xml")
            item = root.find("./channel/item")
            previous = item.findtext(SPARKLE + "version") or item.find("enclosure").get(SPARKLE + "version")
            if int(previous) >= int(metadata["build"]):
                print("Release exists; rolling feed already has this version or a newer version")
                return
        gh("release", "upload", "appcast", str(directory / "appcast.xml"), "--clobber")
    else:
        gh("release", "create", "appcast", str(directory / "appcast.xml"), "--prerelease", "--latest=false",
           "--target", os.environ["GITHUB_SHA"], "--title", "MouseBridge 更新清单",
           "--notes", "Rolling signed update feed. Download the application from a versioned Release.")
    print(f"Published https://github.com/{REPO}/releases/tag/{tag} and updated signed feed")


if __name__ == "__main__":
    publish(sys.argv[1])

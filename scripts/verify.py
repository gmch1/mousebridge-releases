#!/usr/bin/env python3
"""Verify the exact public download payload using only a pinned public key."""
import base64
import hashlib
import json
import pathlib
import plistlib
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile

PUBLIC_KEY = "p5C1GSj0p2P2eVmKlMIc4yJrNOIjdf3+dqgrMowLfm0="
REPO = "gmch1/mousebridge-releases"
SPARKLE = "{http://www.andymatuschak.org/xml-namespaces/sparkle}"


def verify_signature(data, signature):
    signature = base64.b64decode(signature, validate=True)
    if len(signature) != 64:
        raise ValueError("Invalid Ed25519 signature length")
    with tempfile.TemporaryDirectory() as temporary:
        root = pathlib.Path(temporary)
        (root / "key.der").write_bytes(bytes.fromhex("302a300506032b6570032100") + base64.b64decode(PUBLIC_KEY))
        (root / "signature").write_bytes(signature)
        (root / "content").write_bytes(data)
        # macOS ships LibreSSL; GitHub's Mac runners also provide OpenSSL 3.
        openssl = next((p for p in ["/opt/homebrew/opt/openssl@3/bin/openssl",
                        "/usr/local/opt/openssl@3/bin/openssl"] if pathlib.Path(p).is_file()), "openssl")
        subprocess.run([openssl, "pkeyutl", "-verify", "-pubin", "-keyform", "DER",
            "-inkey", str(root / "key.der"), "-rawin", "-in", str(root / "content"),
            "-sigfile", str(root / "signature")], check=True, stdout=subprocess.DEVNULL)


def verify(directory):
    directory = pathlib.Path(directory)
    metadata = json.loads((directory / "release.json").read_text())
    version = metadata["version"]
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version) or metadata["tag"] != "v" + version:
        raise ValueError("Invalid version/tag")
    major, minor, patch = map(int, version.split("."))
    build = str(major * 1_000_000 + minor * 1000 + patch)
    if minor > 999 or patch > 999 or metadata["build"] != build or type(metadata["prerelease"]) is not bool:
        raise ValueError("Invalid release metadata")
    binary = f"MouseBridge-v{version}-macOS.zip"
    source = f"MouseBridge-v{version}-source.zip"
    assets = [binary, binary + ".sha256", source, source + ".sha256", "appcast.xml"]
    if {p.name for p in directory.iterdir()} != set(assets + ["release.json", "notes.md"]):
        raise ValueError("Unexpected publication files")
    for name in (binary, source):
        expected = f"{hashlib.sha256((directory / name).read_bytes()).hexdigest()}  {name}\n"
        if (directory / (name + ".sha256")).read_text() != expected:
            raise ValueError("Checksum mismatch: " + name)
    feed = (directory / "appcast.xml").read_bytes()
    content, separator, footer = feed.rpartition(b"<!-- sparkle-signatures:\n")
    if not separator or not footer.rstrip().endswith(b"-->"):
        raise ValueError("Unsigned update feed")
    fields = dict(line.strip().split(b":", 1) for line in footer.split(b"-->", 1)[0].splitlines() if b":" in line)
    if int(fields[b"length"]) != len(content):
        raise ValueError("Signed feed length mismatch")
    verify_signature(content, fields[b"edSignature"].strip())
    root = ET.fromstring(content)
    items = root.findall("./channel/item")
    if len(items) != 1:
        raise ValueError("Expected one update item")
    item = items[0]
    enclosure = item.find("enclosure")
    expected_url = f"https://github.com/{REPO}/releases/download/v{version}/{binary}"
    if enclosure is None or enclosure.get("url") != expected_url:
        raise ValueError("Unexpected update download URL")
    for key, value in [("version", build), ("shortVersionString", version)]:
        if (item.findtext(SPARKLE + key) or enclosure.get(SPARKLE + key)) != value:
            raise ValueError("Feed version does not match release metadata")
    archive_bytes = (directory / binary).read_bytes()
    if int(enclosure.get("length", "0")) != len(archive_bytes):
        raise ValueError("Update size mismatch")
    verify_signature(archive_bytes, enclosure.get(SPARKLE + "edSignature", ""))
    with zipfile.ZipFile(directory / binary) as archive:
        info = plistlib.loads(archive.read("MouseBridge.app/Contents/Info.plist"))
    if (info["CFBundleShortVersionString"], info["CFBundleVersion"], info["SUPublicEDKey"]) != (version, build, PUBLIC_KEY):
        raise ValueError("Packaged app version/key mismatch")
    if info["SUFeedURL"] != f"https://github.com/{REPO}/releases/download/appcast/appcast.xml":
        raise ValueError("Packaged app feed URL mismatch")
    with zipfile.ZipFile(directory / source) as archive:
        source_info = plistlib.loads(archive.read(f"MouseBridge-v{version}/Info.plist"))
    if source_info["CFBundleShortVersionString"] != version:
        raise ValueError("Corresponding source version mismatch")
    return metadata, assets


if __name__ == "__main__":
    verify(sys.argv[1])
    print("Publication payload and both Ed25519 signatures verified")

#!/usr/bin/env python3
"""BSL syntax only; does not execute code or emulate the 1C platform.

Requires Python 3 and Java 21+ with source-file launcher/compiler.
Artifacts are pinned and verified against Maven Central SHA-256 files.
"""
from pathlib import Path
import hashlib
import os
import subprocess
import sys
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = (
    "io/github/1c-syntax/bsl-parser/0.39.0/bsl-parser-0.39.0.jar",
    "io/github/1c-syntax/antlr4/0.4.0/antlr4-0.4.0.jar",
    "io/github/1c-syntax/utils/0.7.0/utils-0.7.0.jar",
    "org/jspecify/jspecify/1.0.0/jspecify-1.0.0.jar",
)


def main():
    cache = Path(os.environ.get("BSL_CHECK_CACHE", str(Path(tempfile.gettempdir()) / "yandexmodule-bsl-check")))
    cache.mkdir(parents=True, exist_ok=True)
    jars = []
    for artifact in ARTIFACTS:
        url = "https://repo.maven.apache.org/maven2/" + artifact
        with urllib.request.urlopen(url + ".sha256", timeout=30) as response:
            expected = response.read().decode("ascii").strip().split()[0]
        jar = cache / artifact.rsplit("/", 1)[-1]
        if not jar.exists() or hashlib.sha256(jar.read_bytes()).hexdigest() != expected:
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != expected:
                raise RuntimeError("SHA-256 mismatch: " + artifact)
            jar.write_bytes(data)
        jars.append(str(jar))
    files = sys.argv[1:] or [str(p) for directory in ("src", "examples", "tests")
                            for p in sorted((ROOT / directory).rglob("*.bsl"))]
    if not files:
        raise RuntimeError("No BSL files selected")
    return subprocess.run(["java", "-cp", os.pathsep.join(jars),
                           str(ROOT / "tools/CheckBsl.java"), *files], check=False).returncode


if __name__ == "__main__":
    sys.exit(main())

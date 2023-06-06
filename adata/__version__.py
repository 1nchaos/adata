# -*- coding: utf-8 -*-

VERSION = (0, 0, 23)
# PRERELEASE = None  # alpha, beta or rc
PRERELEASE = 'beta'  # alpha, beta or rc
REVISION = None


def generate_version(version, prerelease=None, revision=None):
    version_parts = [".".join(map(str, version))]
    if prerelease is not None:
        version_parts.append(f"-{prerelease}")
    if revision is not None:
        version_parts.append(f".{revision}")
    return "".join(version_parts)

__title__ = "adata"
__description__ = "A Data,A Stock,ETF,Bond,Quant"
__url__ = "https://github.com/1nchaos/adata"
__version__ = generate_version(VERSION, prerelease=PRERELEASE, revision=REVISION)
__author__ = "1nchaos"
__author_email__ = "9527@1nchaos.com"
__license__ = "Apache License"

#!/usr/bin/python
#
# Copyright 2024 - 2025 Khalil Estell and the libhal contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import subprocess

from pathlib import Path
from conan.api.conan_api import ConanAPI, ProfilesAPI, ConfigAPI
from conan.api.model import Remote
from conan.errors import ConanException
from conan.cli.command import conan_command, conan_subcommand

logger = logging.getLogger(__name__)


@conan_subcommand()
def hal_setup(conan_api: ConanAPI, parser, subparser, *args):
    """
    Set up libhal development environment (remotes + profiles)
    """

    logger.info("Setting up libhal environment...")

    REPO = "https://libhal.jfrog.io/artifactory/api/conan/trunk-conan"
    REMOTE_NAME = "libhal"

    logger.info("📦 Adding libhal-trunk to conan remotes...")
    REPO_REMOTE = Remote(REMOTE_NAME, REPO)
    logger.debug(f"Remote URL: {REPO}")

    def remote_exists(conan_api: ConanAPI, remote_name: str):
        try:
            conan_api.remotes.get(remote_name)
            return True
        except Exception:
            return False

    try:
        if remote_exists(conan_api, REMOTE_NAME):
            logger.debug(
                f"Remote '{REMOTE_NAME}' already exists, updating...")
            conan_api.remotes.update(REMOTE_NAME, url=REPO)
            logger.info(f"✅ Remote '{REMOTE_NAME}' updated successfully")
        else:
            logger.debug(
                f"Remote '{REMOTE_NAME}' does not exist, adding...")
            conan_api.remotes.add(REPO_REMOTE)
            logger.info(f"✅ Remote '{REMOTE_NAME}' added successfully")
    except Exception as e:
        logger.error(f"❌ Failed to configure remote: {e}")
        return

    profile_api = ProfilesAPI(conan_api)

    try:
        # If this succeeds then there is nothing to do. If it fails, then we
        # should create a default host profile for the user.
        profile_api.get_default_host()
        logger.info("✅ System already has a default host profile, proceeding!")
    except ConanException:
        logger.info("❌ Default host profile NOT found! Generating one now!")
        HOME_PATH = Path(ConfigAPI(conan_api).home())
        DEFAULT_PROFILE_PATH = HOME_PATH / "profiles" / "default"
        DETECTED_PROFILE_INFO = profile_api.detect()
        DEFAULT_PROFILE_PATH.write_text(str(DETECTED_PROFILE_INFO))
        logger.info("✅ Default profile generated!")
        logger.debug(f"🔍 Profile Contents:\n{DETECTED_PROFILE_INFO}")

    logger.info("✅ libhal environment setup COMPLETE 🚀")


@conan_subcommand()
def hal_update(conan_api: ConanAPI, parser, subparser, *args):
    """
    Update the libhal conan configuration to the latest version
    """

    subparser.add_argument('--tag',
                           help='Specific release tag to install (optional)')
    args = parser.parse_args(*args)

    logger.info("📥 Updating libhal conan configuration...")

    # Build the conan config install command
    CONFIG_URL = 'https://github.com/libhal/conan-config2.git'
    cmd = ['conan', 'config', 'install', CONFIG_URL]

    # Add tag argument if specified
    if args.tag:
        cmd.extend(['--args', f'branch={args.tag}'])
        logger.info(f"Installing from: {CONFIG_URL} (tag: {args.tag})")
    else:
        logger.info(f"Installing from: {CONFIG_URL} (latest)")
    try:
        # Run the command
        logger.debug(cmd)
        result = subprocess.run(cmd, timeout=60)
        if result.returncode == 0:
            logger.info("✅ Configuration updated successfully!")
        else:
            logger.error("❌ Failed to update configuration")
            return 1
    except subprocess.TimeoutExpired:
        logger.error("❌ Update timed out after 60 seconds")
        return 1
    except Exception as e:
        logger.error(f"❌ Error during update: {e}")
        return 1

    return 0


@conan_subcommand()
def hal_flash(conan_api: ConanAPI, parser, subparser, *args):
    """
    Flash binary to target device
    """
    subparser.add_argument('--profile', required=True,
                           help='Profile of the binary to flash')
    subparser.add_argument('--port', help='Serial port for flashing')
    subparser.add_argument('--binary', help='Path to binary file')
    subparser.add_argument('--verify', action='store_true',
                           help='Verify after flashing')
    args = parser.parse_args(*args)

    logger.info(f"Flashing to device on {args.port}...")
    logger.info("TODO: Implement flash command")


@conan_subcommand()
def hal_debug(conan_api: ConanAPI, parser, subparser, *args):
    """
    Start debug session with target device
    """
    subparser.add_argument('--profile', help='Profile to debug')
    subparser.add_argument('--port', help='Debug port')
    subparser.add_argument('--gdb', action='store_true', help='Use GDB')
    args = parser.parse_args(*args)

    logger.info("Starting debug session...")
    logger.info("TODO: Implement debug command")


@conan_command(group="libhal")
def hal(conan_api: ConanAPI, parser, *args):
    """
    libhal development tools for embedded systems
    """
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='conan-config2: 1.1.1',
        help='Show version and exit'
    )

    parser.epilog = """
Examples:
  conan hal setup
  conan hal update

Use "conan hal <command> --help" for more information on a specific command.
"""

    # Parse args to get verbose flag
    parsed_args, _ = parser.parse_known_args(*args)

    # Configure logging based on verbose flag
    log_level = logging.DEBUG if parsed_args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(message)s',
        force=True
    )

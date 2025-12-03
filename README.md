# Welcome to the conan-config2

## Installation

To install the libhal conan configuration (recommended if you want to use
libhal), execute this command in your command line:

```bash
conan config install https://github.com/libhal/conan-config2.git
```

This will install all of the latest profiles and custom settings for libhal development.

## About This Repository

This repository contains Conan 2.x configuration files for libhal development.
It does **not** have a README.md file because that would result in it being
picked up by `conan config install` and placed in your Conan home directory.
Instead, we use this wiki for documentation.

The repository follows the official Conan 2 home directory layout with regards
to placement of the `profiles` and `settings_user.yml` files.

## What's Included

### 🔧 `conan hal` command

#### `conan hal setup`

Set up your libhal development environment by configuring remotes and installing profiles.

**What it does:**

1. Adds/updates the `libhal` remote repository
2. Generates and installs default system profile if it does not already exist.

#### `conan hal update`

This is a short hand for the conan config install command above. This will
simply call `conan config install https://github.com/libhal/conan-config2.git`
which will update this command and all of the profiles.

### Custom Settings (`settings_user.yml`)

- **Architecture settings**: Support for ARM Cortex-M processors (M0, M0+, M1, M3, M4, M4F, M7, M7F, M7D, M23, M33, M33F, M35PF, M55, M85)
- (DEPRECATED) ~~**libc settings**: Options for null, default, or custom C library implementations~~

### Profiles

The configuration includes profiles organized into four categories under
`profiles/hal/`:

#### 1. **MCU Profiles** (`profiles/hal/mcu/`)

Target-specific profiles for microcontrollers including:

- **LPC40 series**: lpc4072, lpc4074, lpc4076, lpc4078, lpc4088
- **STM32 series**: stm32f103c4, stm32f103c6, stm32f103c8, and more
- _More series to come..._

#### 2. **Toolchain Profiles** (`profiles/hal/tc/`)

Compiler toolchain configurations:

- **ARM GCC**: Multiple versions (11.3, 12.2, 12.3, 13.2, 13.3, 14.2)
- **LLVM**: Latest versions (19.1.7, 20.1.8)

#### 3. **BSP Profiles** (`profiles/hal/bsp/`)

Board Support Package profiles:

- mod-lpc40-v5
- mod-stm32f1-v4, mod-stm32f1-v5

#### 4. **OS Profiles** (`profiles/hal/os/`)

Host operating system profiles for native development:

- Linux (ARM, x86_64)
- macOS (ARM, x86_64)
- Windows (ARM, x86_64)

## Using the Profiles

After installation, you can use these profiles with the `-pr` flags:

```bash
# Build for an LPC4078 with ARM GCC (latest which is 14.2)
conan install . -pr=hal/mcu/lpc4078 -pr=hal/tc/arm-gcc

# Build for a LPC4078 MicroMod board support library using ARM GCC 13.2
conan install . -pr=hal/bsp/mod-lpc40-v5 -pr=hal/tc/arm-gcc-13.2

# Native build for your OS using the latest LLVM available via llvm-toolchain
conan install . -pr=hal/os/linux_x86_64 -pr llvm
```

## Verifying Installation

To verify the profiles were installed correctly:

```bash
conan profile list
```

You should see profiles under the `hal/` directory.

To check the location of your Conan home directory:

```bash
conan config home
```

## Updating the Configuration

To update to the latest profiles:

```bash
conan config install https://github.com/libhal/conan-config2.git
```

This will overwrite existing configuration with the latest version.

## Additional Resources

- [libhal Documentation](https://libhal.github.io/libhal)
- [Conan 2.x Documentation](https://docs.conan.io/2/)
- [libhal Organization](https://github.com/libhal)

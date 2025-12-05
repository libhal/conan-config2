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

Compiler toolchain configurations with multiple tiers:

**Sliding window profiles** (for prebuilt binary compatibility):

- `llvm`, `arm-gcc` - Current recommended stable version
- `llvm-prev`, `arm-gcc-prev` - Previous major version (extended support)
- `llvm-next`, `arm-gcc-next` - Next major version (early adopter)

> [!note]
> Currently all three point to the same version (llvm-20, arm-gcc-14) as
> the sliding window is being established. These profiles will differentiate as
> new major versions are released.

**Base version profiles** (auto-select latest minor/patch version):

- `arm-gcc-14`, `arm-gcc-13` - Major version with automatic minor selection
- `llvm-20`, `llvm-19` - Major version with automatic minor selection

**Specific version profiles** (exact version locking):

- **ARM GCC**: 11.3, 12.2, 12.3, 13.2, 13.3, 14.2, 14.3
- **LLVM**: 19.1.5, 19.1.7, 20.1.8

See the "Toolchain Version Strategy" section below for guidance on which to use.

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
# Build for an LPC4078 with latest ARM GCC 14.x available for your platform
conan install . -pr=hal/mcu/lpc4078 -pr=hal/tc/arm-gcc-14

# Build for a LPC4078 MicroMod board with specific ARM GCC version
conan install . -pr=hal/bsp/mod-lpc40-v5 -pr=hal/tc/arm-gcc-14.3

# Native build for your OS using latest LLVM 20.x available
conan install . -pr=hal/os/linux_x86_64 -pr=hal/tc/llvm-20

# Use current recommended toolchains (currently llvm-20 and arm-gcc-14)
conan install . -pr=hal/mcu/stm32f103c8 -pr=hal/tc/llvm
```

### Toolchain Version Strategy

#### Base vs Specific Versions

**Base version profiles** (e.g., `arm-gcc-14`, `llvm-20`) use Conan version
ranges to automatically select the latest available minor/patch version for your
target platform:

- ARM Cortex-M targets might get 20.1.5 while x86_64 gets 20.1.8
- You automatically benefit from new minor versions without profile changes
- Recommended for most development workflows

**Specific version profiles** (e.g., `arm-gcc-14.3`, `llvm-20.1.8`) lock to
exact versions:

- Use when you need reproducible builds across all platforms
- Useful for CI/CD pipelines or release builds
- Pair with `conan lock` for complete dependency locking

#### Prebuilt Binary Support & Sliding Window

libhal maintains prebuilt binaries for a **sliding window of compiler**
**versions** to balance resource usage with backward compatibility:

- **`llvm`/`arm-gcc`**: Current recommended stable version (e.g., llvm-20,
  arm-gcc-14)
- **`llvm-prev`/`arm-gcc-prev`**: Previous major version (coming soon - ensures
  users on older versions continue getting prebuilts)
- **`llvm-next`/`arm-gcc-next`**: Next major version (coming soon - for early
  adopters testing upcoming compilers)

Prebuilts are built against these three profiles. Users on specific base
versions (e.g., `llvm-20`) will receive prebuilt support until that version
ages out of the window, at which point we'll provide migration notices.

**Example migration path:**

1. Today: `llvm-20` is current, prebuilts available
2. LLVM 22 is released and LLVM 21 becomes the new current releases
3. Migration path:
   1. `llvm-prev` → `llvm-20`
   2. `llvm` → `llvm-21`
   3. `llvm-next` → `llvm-22`
4. Users on `llvm-20` continue getting prebuilts via `llvm-prev`
5. Eventually: `llvm-20` ages out, migration notice provided

#### Which Profile Should You Use?

**For application/project development:**

- Use **current version profiles** (e.g., `llvm`, `arm-gcc`) to ensure
  maximum compatibility with libhal ecosystem libraries (recommended - all
  prebuilts available)
- Use **base version profiles** (e.g., `llvm-20`, `arm-gcc-14`) for stability
  within a major version while getting minor updates (some libraries may
  require building from source)
- Use **specific versions** (e.g., `llvm-20.1.8`) for complete reproducibility
  in production/release builds (imported libraries will likely require building
  from source)

**For library development or staying current:**

- Use **`llvm`/`arm-gcc`** to always track the currently recommended stable
  version
- Use **`llvm-next`/`arm-gcc-next`** to test compatibility with upcoming
  versions
- Use **`llvm-prev`/`arm-gcc-prev`** if you need extra time before upgrading
  (note: this will eventually auto-upgrade when the window slides)

> [!important]
> All sliding window profiles (`llvm`, `llvm-prev`, `llvm-next`) will
> eventually force major version upgrades as the support window moves. For
> long-term version stability within a major release, use base version profiles
> like `llvm-20`.

#### Upgrade Frequency

Currently, toolchain versions are updated as frequently as upstream releases
allow while the libhal ecosystem is growing. As the user base expands, we
expect to stabilize around ~6-month cycles between major version upgrades,
dependent on upstream release schedules from ARM, LLVM, RISC-V, and Xtensa
toolchain providers.

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

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

The configuration includes profiles organized into five categories under
`profiles/hal/`:

#### 1. **Bare Metal Profiles** (`profiles/hal/bare/`)

Architecture-specific bare metal profiles for direct hardware targeting without
an MCU-specific configuration:

- cortex-m0, cortex-m0plus, cortex-m1, cortex-m3, cortex-m4, cortex-m4f
- cortex-m7, cortex-m7d, cortex-m7f
- cortex-m23, cortex-m33, cortex-m33f, cortex-m35p, cortex-m35pf
- cortex-m55, cortex-m85

These profiles set only the architecture and baremetal OS, allowing maximum
flexibility for custom hardware configurations.

#### 2. **MCU Profiles** (`profiles/hal/mcu/`)

Target-specific profiles for microcontrollers including:

- **LPC40 series**: lpc4072, lpc4074, lpc4076, lpc4078, lpc4088
- **STM32 series**: stm32f103c4, stm32f103c6, stm32f103c8, and more
- _More series to come..._

> [!important]
> When using MCU profiles, use the `-pr:a` (apply to all) flag instead of `-pr`
> (host only). This ensures the profile is applied to both build and host
> contexts, allowing the context-aware logic to properly configure each
> environment. Using `-pr` would only apply to the host context and miss
> build-time configuration.

#### 3. **Toolchain Profiles** (`profiles/hal/tc/`)

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

#### 4. **BSP Profiles** (`profiles/hal/bsp/`)

Board Support Package profiles:

- mod-lpc40-v5
- mod-stm32f1-v4, mod-stm32f1-v5

> [!important]
> When using MCU profiles, use the `-pr:a` (apply to all) flag instead of `-pr`
> (host only). This ensures the profile is applied to both build and host
> contexts, allowing the context-aware logic to properly configure each
> environment. Using `-pr` would only apply to the host context and miss
> build-time configuration.

#### 5. **OS Profiles** (`profiles/hal/os/`)

Host operating system profiles for native development:

**Auto-detecting profiles** (recommended for most users):

- `linux` - Automatically detects your Linux architecture (ARM or x86_64)
- `mac` - Automatically detects your macOS architecture (ARM or x86_64)
- `windows` - Automatically detects your Windows architecture (ARM or x86_64)

**Architecture-specific profiles** (for explicit control or cross-compilation):

- `linux_arm`, `linux_x86_64`
- `mac_arm`, `mac_x86_64`
- `windows_arm`, `windows_x86_64`

## Using the Profiles

After installation, you can use these profiles with the `-pr` flags:

```bash
# Build for an LPC4078 with latest ARM GCC 14.x available for your platform
conan install . -pr:a=hal/mcu/lpc4078 -pr=hal/tc/arm-gcc-14

# Build for a LPC4078 MicroMod board with specific ARM GCC version
conan install . -pr:a=hal/bsp/mod-lpc40-v5 -pr=hal/tc/arm-gcc-14

# Build for bare metal Cortex-M85 with current LLVM
conan install . -pr=hal/bare/cortex-m85 -pr=hal/tc/llvm

# Native build for your OS with auto-detection using latest LLVM 20.x available
conan install . -pr=hal/os/linux -pr=hal/tc/llvm-20

# Native build for specific architecture (e.g., cross-compiling for ARM on x86_64)
conan install . -pr=hal/os/linux_arm -pr=hal/tc/llvm-20

# Use current toolchains
conan install . -pr:a=hal/mcu/stm32f103c8 -pr=hal/tc/llvm
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

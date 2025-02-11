# coding: utf-8
import platform


__all__ = ('PSYDAC_DEFAULT_FOLDER', 'PSYDAC_BACKENDS')

#==============================================================================

PSYDAC_DEFAULT_FOLDER = {'name':'__psydac__'}

# ... defining PSYDAC backends
PSYDAC_BACKEND_PYTHON = {'name': 'python', 'tag':'python', 'openmp':False}

PSYDAC_BACKEND_GPYCCEL  = {'name': 'pyccel',
                       'compiler': 'GNU',
                       'flags'   : '-O3 -ffast-math',
                       'folder'  : '__gpyccel__',
                       'tag'     : 'gpyccel',
                       'openmp'  : False}

PSYDAC_BACKEND_IPYCCEL  = {'name': 'pyccel',
                       'compiler': 'intel',
                       'flags'   : '-O3',
                       'folder'  : '__ipyccel__',
                       'tag'     :'ipyccel',
                       'openmp'  : False}

PSYDAC_BACKEND_PGPYCCEL = {'name': 'pyccel',
                       'compiler': 'PGI',
                       'flags'   : '-O3 -Munroll',
                       'folder'  : '__pgpyccel__',
                       'tag'     : 'pgpyccel',
                       'openmp'  : False}

PSYDAC_BACKEND_NVPYCCEL = {'name': 'pyccel',
                       'compiler': 'nvidia',
                       'flags'   : '-O3 -Munroll',
                       'folder'  : '__nvpyccel__',
                       'tag'     : 'nvpyccel',
                       'openmp'  : False}
# ...

# Platform-dependent flags
if platform.system() == "Darwin" and platform.machine() == 'arm64':
    # Apple silicon requires architecture-specific flags (see https://github.com/pyccel/psydac/pull/411)
    import subprocess # nosec B404
    cpu_brand = subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string']).decode('utf-8') # nosec B603, B607
    if "Apple M1" in cpu_brand:
        PSYDAC_BACKEND_GPYCCEL['flags'] += ' -mcpu=apple-m1'
    else:
        # TODO: Support later Apple CPU models. Perhaps the CPU naming scheme could be easily guessed
        # based on the output of 'sysctl -n machdep.cpu.brand_string', but I wouldn't rely on this
        # guess unless it has been manually verified. Loud errors are better than silent failures!
        raise SystemError(f"Unsupported Apple CPU '{cpu_brand}'.")
else:
    # Default architecture flags
    PSYDAC_BACKEND_GPYCCEL['flags'] += ' -march=native -mtune=native'
    if platform.machine() == 'x86_64':
        PSYDAC_BACKEND_GPYCCEL['flags'] += ' -mavx'

#==============================================================================

# List of all available backends for accelerating Python code
PSYDAC_BACKENDS = {
    'python'       : PSYDAC_BACKEND_PYTHON,
    'pyccel-gcc'   : PSYDAC_BACKEND_GPYCCEL,
    'pyccel-intel' : PSYDAC_BACKEND_IPYCCEL,
    'pyccel-pgi'   : PSYDAC_BACKEND_PGPYCCEL,
    'pyccel-nvidia': PSYDAC_BACKEND_NVPYCCEL,
}

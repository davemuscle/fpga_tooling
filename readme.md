# fpga_tooling
## Install
Required:
- Add fpga_tooling/bin to your PATH
- Add fpga_tooling/bin to your PYTHONPATH

Optional:
- Add an alias for 'lint.sh' to 'lint'

Example, add to ~/.bashrc:
```
    export FPGA_TOOL_PATH="/home/dave/fpga_tooling/bin"
    export PATH="$PATH:$FPGA_TOOL_PATH"
    export PYTHONPATH="PYTHON:$FPGA_TOOL_PATH"
    alias lint="lint.sh"
``` 

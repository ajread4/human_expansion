# Human Expansion

Plugin supplying CALDERA with human emulation capabilities based on [Human](https://github.com/mitre/caldera/wiki/Plugins-human) and [here](https://github.com/mitre/human). 

# Changes to Human

The sections describe my changes that have been made for Human.

# Workflows 
- added run_echo.py, run_os.py, run_powershell.py 
# Data
- Added user behaviors to describe common user activity on a host
- Added os_commands, powershell_commands, echo_words, file_options, dir_options
  - echo_words comes from [here](https://www.mit.edu/~ecprice/wordlist.10000). 
  - powershell_commands is from [here](https://activedirectorypro.com/powershell-commands/).
  - os_commands is from [here](https://www.lifewire.com/dos-commands-4070427)
  - file_options and dir_options are from [here](https://github.com/emadshanab/WordLists-20111129)
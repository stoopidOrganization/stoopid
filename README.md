# <img src="images/stoopidlogomd.png" width="32" height="32">TOOPID

---

Usage
: (python version) `python stoopid.py <filename>`
: (exe) `stoopid.exe <filename>`

Aditional Parameters
| Parameter | Description |
| --------- | ----------- |
| --log \<filename\> | file to write the logs to |
| --silent | disables all output |

Commands
| Keyword | Syntax | Description |
| ------- | ------ | ----------- |
| var | `var : <name> = <value>` | Creates a variable |
| arr | `arr : <name> : <size>` | Creates an array |
| app | `app : <name> : value` | Appends to an array |
| getarr | `getarr : <name> : <index> : <destination>` | Gets the value of an array at index |
| out | `out : <name>` | Prints the given value |
| goto | `goto : <line>` | Changes the next line read by the interpreter |
| sleep | `sleep : <time>` | Waits the given time until next execution |
| math | `math <destination> : <value1> <operator <value2>` | Caluclates given Operation and set it to a variable |

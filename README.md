# <img src="./images/stoopidlogomd.png" width="32" height="32">TOOPID
---
##### Usage:
- Python: `python stoopid.py <filename>`
- Executable: `stoopid.exe <filename>`
##

# DISCLAIMER:
### Due to a temporary math solving algorythm which uses funcitons which are considered
### risky, the exe currently might be detected as a virus.
### Dont wory, this is a FALSE POSITIVE, as the source code and tools to build your own exe are open source.
### We are are expecting a new math solving algorythm to be implemented in the near future, which should resolve this issue.


##### Aditional Parameters
| Parameter | Description |
| --------- | ----------- |
| --log \<filename\> | file to write the logs to |
| --silent | disables all output |
##
##### Commands
| Keyword | Syntax | Description |
| ------- | ------ | ----------- |
| var | `var : <name> = <value>` | Creates a variable |
| arr | `arr : <name> : <size>` | Creates an array |
| app | `app : <name> : <value>` | Appends to an array |
| getarr | `getarr : <name> : <index> : <destination>` | Gets the value of an array at index |
| out | `out : <name>` | Prints the given value |
| goto | `goto : <line>` | Changes the next line read by the interpreter |
| sleep | `sleep : <time>` | Waits the given time until next execution |
| math | `math <destination> : <value1> <operator <value2>` | Caluclates given Operation and set it to a variable |
| goif | `goif : <line> : <condition>` | Changes the next line read by the interpreter if given condition is true |
| if | `if : <condition> : {` | Executes code in curly brackets if the condition is true |
| bool | `bool : <name> = <value>` | Creates a boolean |
| end | `end` | Stops code |
##
##### Other useful features
Comments can be made with a # as the first character: `# this is a comment`
Labels can be added after a line and you can jump to them with `goto` or `goif`: `: <label>`
##
##### Comparators
| Comparator | Example |
| ---------- | ------- |
| << | `1 << 2` |
| >> | `2 >> 1` |
| == | `2 == 2` |
| != | `2 != 1` |
| <= | `1 <= 2` or `1 <= 1` |
| >= | `2 >= 1` or `2 >= 2` |

##
##### Operators
| Operators | Example |
| ---------- | ------- |
| + | `1 + 2 = 3` |
| - | `3 - 2 = 1` |
| * | `3 * 2 = 6` |
| / | `3 / 2 = 1.5` |
| % | `3 % 2 = 1` |
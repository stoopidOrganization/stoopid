
![stoopidlogo](https://user-images.githubusercontent.com/69861550/184194331-30fd7818-ddd2-4f15-8d57-05261de49395.png)

Usage: 
(python version) python stoopid.py <inputfile>

(exe) stoopid.exe <inputfile>

Additional parameters:

--log <logfile> 
   logs the output to a file



The commands of stoopid are:

var : name = value 

arr : name : size

app : name : value

getarr : name : index : destination

string : name = value

out : name

goto : line

sleep : time

math : destination : value1 operator value2

goif : destination : var1  comparator  var2 

import:name

at the end of a line there can be a comment (#)

or a label (:name:label)

wthe comparitors are

<<, >>, ==, !=, <=, >=

the operators are

+ ,-, *, /, %

I should note that the syntax is strict, and can only be written as in the example

eg.: math: a : b+c*d #Invalid because of multiple operators

   math operations have to be split up into their individual paths

   math: a : c*d #the correct way
   
   math: a : a+b


libraries will be executed on each line with the run() function.

the goif function can take many arguments if you append :or: or :and: to the end of the line
The ors and ands are executed strictly left to right.

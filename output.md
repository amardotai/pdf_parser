
<!-- Page 1 -->
36
PART I     The Java Language
You can use these types as-is, or to construct arrays or your own class types. Thus, they
form the basis for all other types of data that you can create.
The primitive types represent single values—not complex objects. Although Java is
otherwise completely object-oriented, the primitive types are not. They are analogous to
the simple types found in most other non–object-oriented languages. The reason for this
is efficiency. Making the primitive types into objects would have degraded performance
too much.
The primitive types are defined to have an explicit range and mathematical behavior.
Languages such as C and C++ allow the size of an integer to vary based upon the dictates
of the execution environment. However, Java is different. Because of Java’s portability
int
requirement, all data types have a strictly defined range. For example, an
is always 32 bits,
regardless of the particular platform. This allows programs to be written that are guaranteed
to run
**without porting**
on any machine architecture. While strictly specifying the size of an
integer may cause a small loss of performance in some environments, it is necessary in
order to achieve portability.
Let’s look at each type of data in turn.
# Integers
byte
short
int
long
Java defines four integer types:
,
,
, and
. All of these are signed, positive
and negative values. Java does not support unsigned, positive-only integers. Many other
computer languages support both signed and unsigned integers. However, Java’s designers
felt that unsigned integers were unnecessary. Specifically, they felt that the concept of
**unsigned**
was used mostly to specify the behavior of the
**high-order bit**
, which defines the
**sign**
of an integer value. As you will see in Chapter 4, Java manages the meaning of the high-
order bit differently, by adding a special “unsigned right shift” operator. Thus, the need for
an unsigned integer type was eliminated.
The
**width**
of an integer type should not be thought of as the amount of storage it
consumes, but rather as the
**behavior**
it defines for variables and expressions of that type.
The Java run-time environment is free to use whatever size it wants, as long as the types
behave as you declared them. The width and ranges of these integer types vary widely, as
shown in this table:
|Name|Width|Range|
|---|---|---|
|**long**|64|–9,223,372,036,854,775,808 to 9,223,372,036,854,775,807|
|**int**|32|–2,147,483,648 to 2,147,483,647|
|**short**|16|–32,768 to 32,767|
|**byte**|8|–128 to 127|


Let’s look at each type of integer.
## byte
byte
The smallest integer type is
. This is a signed 8-bit type that has a range from –128 to
byte
127. Variables of type
are especially useful when you’re working with a stream of data
from a network or file. They are also useful when you’re working with raw binary data that
may not be directly compatible with Java’s other built-in types.

---

<!-- Page 2 -->
37
Chapter 3     Data Types, Variables, and Arrays
byte
Byte variables are declared by use of the
keyword. For example, the following
byte
b
c
declares two
variables called
and
:
### Part I
byte b, c;
## short
short
is a signed 16-bit type. It has a range from –32,768 to 32,767. It is probably the least-
short
used Java type. Here are some examples of
variable declarations:
short s;
short t;
## int
int
The most commonly used integer type is
. It is a signed 32-bit type that has a range
int
from –2,147,483,648 to 2,147,483,647. In addition to other uses, variables of type
are
commonly employed to control loops and to index arrays. Although you might think that
byte
short
int
using a
or
would be more efficient than using an
in situations in which the
int
byte
larger range of an
is not needed, this may not be the case. The reason is that when
short
int
and
values are used in an expression, they are
**promoted**
to
when the expression is
int
evaluated. (Type promotion is described later in this chapter.) Therefore,
is often the
best choice when an integer is needed.
## long
long
int
is a signed 64-bit type and is useful for those occasions where an
type is not large
long
enough to hold the desired value. The range of a
is quite large. This makes it useful
when big, whole numbers are needed. For example, here is a program that computes the
number of miles that light will travel in a specified number of days:
// Compute distance light travels using long variables.
class Light {
public static void main(String args[]) {
int lightspeed;
long days;
long seconds;
long distance;
// approximate speed of light in miles per second
lightspeed = 186000;
days = 1000; // specify number of days here
seconds = days * 24 * 60 * 60; // convert to seconds
distance = lightspeed * seconds; // compute distance
System.out.print("In " + days);
System.out.print(" days light will travel about ");
System.out.println(distance + " miles.");
}
}

---

<!-- Page 3 -->
38
PART I     The Java Language
This program generates the following output:
In 1000 days light will travel about 16070400000000 miles.
int
Clearly, the result could not have been held in an
variable.
# Floating-Point Types
Floating-point numbers, also known as
**real**
numbers, are used when evaluating expressions
that require fractional precision. For example, calculations such as square root, or
transcendentals such as sine and cosine, result in a value whose precision requires a floating-
point type. Java implements the standard (IEEE–754) set of floating-point types and
float
double
operators. There are two kinds of floating-point types,
and
, which represent
single- and double-precision numbers, respectively. Their width and ranges are shown here:
|Name|Width in Bits|Approximate Range|
|---|---|---|
|**double**|64|4.9e–324 to 1.8e+308|
|**float**|32|1.4e–045 to 3.4e+038|


Each of these floating-point types is examined next.
## float
float
The type
specifies a
**single-precision**
value that uses 32 bits of storage. Single precision is
faster on some processors and takes half as much space as double precision, but will become
float
imprecise when the values are either very large or very small. Variables of type
are
useful when you need a fractional component, but don’t require a large degree of precision.
float
For example,
can be useful when representing dollars and cents.
float
Here are some example
variable declarations:
float hightemp, lowtemp;
## double
double
Double precision, as denoted by the
keyword, uses 64 bits to store a value. Double
precision is actually faster than single precision on some modern processors that have been
optimized for high-speed mathematical calculations. All transcendental math functions,
sin( )
cos( )
sqrt( )
double
such as
,
, and
, return
values. When you need to maintain accuracy
double
over many iterative calculations, or are manipulating large-valued numbers,
is the
best choice.
double
Here is a short program that uses
variables to compute the area of a circle:
// Compute the area of a circle.
class Area {
public static void main(String args[]) {
double pi, r, a;
r = 10.8; // radius of circle
pi = 3.1416; // pi, approximately

---

<!-- Page 4 -->
39
Chapter 3     Data Types, Variables, and Arrays
a = pi * r * r; // compute area
System.out.println("Area of circle is " + a);
### Part I
}
}
# Characters
char
In Java, the data type used to store characters is
. However, C/C++ programmers
char
char
char
beware:
in Java is not the same as
in C or C++. In C/C++,
is 8 bits wide. This
is
**not**
the case in Java. Instead, Java uses
**Unicode**
to represent characters. Unicode defines a
fully international character set that can represent all of the characters found in all human
languages. It is a unification of dozens of character sets, such as Latin, Greek, Arabic, Cyrillic,
Hebrew, Katakana, Hangul, and many more. At the time of Java's creation, Unicode required
char
char
16 bits. Thus, in Java
is a 16-bit type. The range of a
is 0 to 65,536. There are no
char
negative
s. The standard set of characters known as ASCII still ranges from 0 to 127 as
always, and the extended 8-bit character set, ISO-Latin-1, ranges from 0 to 255. Since Java is
designed to allow programs to be written for worldwide use, it makes sense that it would use
Unicode to represent characters. Of course, the use of Unicode is somewhat inefficient for
languages such as English, German, Spanish, or French, whose characters can easily be
contained within 8 bits. But such is the price that must be paid for global portability.
More information about Unicode can be found at http://www.unicode.org.
NOTE
char
Here is a program that demonstrates
variables:
// Demonstrate char data type.
class CharDemo {
public static void main(String args[]) {
char ch1, ch2;
ch1 = 88; // code for X
ch2 = 'Y';
System.out.print("ch1 and ch2: ");
System.out.println(ch1 + " " + ch2);
}
}
This program displays the following output:
ch1 and ch2: X Y
ch1
Notice that
is assigned the value 88, which is the ASCII (and Unicode) value that
corresponds to the letter
**X**
. As mentioned, the ASCII character set occupies the first 127
values in the Unicode character set. For this reason, all the “old tricks” that you may have
used with characters in other languages will work in Java, too.

---

<!-- Page 5 -->
40
PART I     The Java Language
char
Although
is designed to hold Unicode characters, it can also be used as an integer
type on which you can perform arithmetic operations. For example, you can add two
characters together, or increment the value of a character variable. Consider the following
program:
// char variables behave like integers.
class CharDemo2 {
public static void main(String args[]) {
char ch1;
ch1 = 'X';
System.out.println("ch1 contains " + ch1);
ch1++; // increment ch1
System.out.println("ch1 is now " + ch1);
}
}
The output generated by this program is shown here:
ch1 contains X
ch1 is now Y
ch1
ch1
ch1
In the program,
is first given the value
**X**
. Next,
is incremented. This results in
containing
**Y**
, the next character in the ASCII (and Unicode) sequence.
char
In the formal specification for Java,
is referred to as an integral type, which means that it is
NOTE
int
short
long
byte
in the same general category as
,
,
, and
. However, because its principal use is for
char
representing Unicode characters,
is commonly considered to be in a category of its own.
# Booleans
boolean
Java has a primitive type, called
, for logical values. It can have only one of two
true
false
possible values,
or
. This is the type returned by all relational operators, as in the
a < b
boolean
case of
.
is also the type
**required**
by the conditional expressions that govern the
if
for
control statements such as
and
.
boolean
Here is a program that demonstrates the
type:
// Demonstrate boolean values.
class BoolTest {
public static void main(String args[]) {
boolean b;
b = false;
System.out.println("b is " + b);
b = true;
System.out.println("b is " + b);
// a boolean value can control the if statement
if(b) System.out.println("This is executed.");
b = false;

---

<!-- Page 6 -->
41
Chapter 3     Data Types, Variables, and Arrays
if(b) System.out.println("This is not executed.");
// outcome of a relational operator is a boolean value
### Part I
System.out.println("10 > 9 is " + (10 > 9));
}
}
The output generated by this program is shown here:
b is false
b is true
This is executed.
10 > 9 is true
There are three interesting things to notice about this program. First, as you can see,
boolean
println( )
when a
value is output by
, "true" or "false" is displayed. Second, the value
boolean
if
of a
variable is sufficient, by itself, to control the
statement. There is no need to
if
write an
statement like this:
if(b == true) …
<
boolean
Third, the outcome of a relational operator, such as
, is a
value. This is why the
10>9
10>9
expression
displays the value "true." Further, the extra set of parentheses around
+
>
is necessary because the
operator has a higher precedence than the
.
# A Closer Look at Literals
Literals were mentioned briefly in Chapter 2. Now that the built-in types have been formally
described, let’s take a closer look at them.
## Integer Literals
Integers are probably the most commonly used type in the typical program. Any whole
number value is an integer literal. Examples are 1, 2, 3, and 42. These are all decimal values,
meaning they are describing a base 10 number. Two other bases that can be used in integer
literals are
**octal**
(base eight) and
**hexadecimal**
(base 16). Octal values are denoted in Java by a
leading zero. Normal decimal numbers cannot have a leading zero. Thus, the seemingly
valid value 09 will produce an error from the compiler, since 9 is outside of octal’s 0 to 7
range. A more common base for numbers used by programmers is hexadecimal, which
matches cleanly with modulo 8 word sizes, such as 8, 16, 32, and 64 bits. You signify a
0x
0X
hexadecimal constant with a leading zero-x, (
or
). The range of a hexadecimal digit is
0 to 15, so
**A**
through
**F**
(or
**a**
through
**f**
) are substituted for 10 through 15.
int
Integer literals create an
value, which in Java is a 32-bit integer value. Since Java is
strongly typed, you might be wondering how it is possible to assign an integer literal to one
byte
long
of Java’s other integer types, such as
or
, without causing a type mismatch error.
byte
Fortunately, such situations are easily handled. When a literal value is assigned to a
or
short
variable, no error is generated if the literal value is within the range of the target type.
long
long
An integer literal can always be assigned to a
variable. However, to specify a
long
literal, you will need to explicitly tell the compiler that the literal value is of type
. You
do this by appending an upper- or lowercase
**L**
to the literal. For example, 0x7ffffffffffffffL

---

<!-- Page 7 -->
42
PART I     The Java Language
long
char
or 9223372036854775807L is the largest
. An integer can also be assigned to a
as
long as it is within range.
Beginning with JDK 7, you can also specify integer literals using binary. To do so, prefix
0b
0B
the value with
or
. For example, this specifies the decimal value 10 using a binary
literal:
int x = 0b1010;
Among other uses, the addition of binary literals makes it easier to enter values used as
bitmasks. In such a case, the decimal (or hexadecimal) representation of the value does not
visually convey its meaning relative to its use. The binary literal does.
Also beginning with JDK 7, you can embed one or more underscores in an integer
literal. Doing so makes it easier to read large integer literals. When the literal is compiled,
the underscores are discarded. For example, given
int x = 123_456_789;
x
the value given to
will be 123,456,789. The underscores will be ignored. Underscores can
only be used to separate digits. They cannot come at the beginning or the end of a literal. It
is, however, permissible for more than one underscore to be used between two digits. For
example, this is valid:
int x = 123___456___789;
The use of underscores in an integer literal is especially useful when encoding such
things as telephone numbers, customer ID numbers, part numbers, and so on. They are
also useful for providing visual groupings when specifying binary literals. For example,
binary values are often visually grouped in four-digits units, as shown here:
int x = 0b1101_0101_0001_1010;
## Floating-Point Literals
Floating-point numbers represent decimal values with a fractional component. They can be
expressed in either standard or scientific notation.
**Standard notation**
consists of a whole
number component followed by a decimal point followed by a fractional component. For
example, 2.0, 3.14159, and 0.6667 represent valid standard-notation floating-point numbers.
**Scientific notation**
uses a standard-notation, floating-point number plus a suffix that specifies
a power of 10 by which the number is to be multiplied. The exponent is indicated by an
**E**
or
**e**
followed by a decimal number, which can be positive or negative. Examples include
6.022E23, 314159E–05, and 2e+100.
double
float
Floating-point literals in Java default to
precision. To specify a
literal, you
double
must append an
**F**
or
**f**
to the constant. You can also explicitly specify a
literal by
double
appending a
**D**
or
**d**
. Doing so is, of course, redundant. The default
type consumes
float
64 bits of storage, while the smaller
type requires only 32 bits.
Hexadecimal floating-point literals are also supported, but they are rarely used. They
P
p
E
e
must be in a form similar to scientific notation, but a
or
, rather than an
or
, is used.
P
For example, 0x12.2P2 is a valid floating-point literal. The value following the
, called the

---

<!-- Page 8 -->
43
Chapter 3     Data Types, Variables, and Arrays
**binary**
**exponent**
, indicates the power-of-two by which the number is multiplied. Therefore,
0x12.2P2
represents 72.5.
Beginning with JDK 7, you can embed one or more underscores in a floating-point
### Part I
literal. This feature works the same as it does for integer literals, which were just described.
Its purpose is to make it easier to read large floating-point literals. When the literal is
compiled, the underscores are discarded. For example, given
double num = 9_423_497_862.0;
num
the value given to
will be 9,423,497,862.0. The underscores will be ignored. As is the
case with integer literals, underscores can only be used to separate digits. They cannot
come at the beginning or the end of a literal. It is, however, permissible for more than one
underscore to be used between two digits. It is also permissible to use underscores in the
fractional portion of the number. For example,
double num = 9_423_497.1_0_9;
.109
is legal. In this case, the fractional part is
.
## Boolean Literals
boolean
Boolean literals are simple. There are only two logical values that a
value can have,
true
false
true
false
and
. The values of
and
do not convert into any numerical representation.
true
false
The
literal in Java does not equal 1, nor does the
literal equal 0. In Java, the
boolean
Boolean literals can only be assigned to variables declared as
or used in expressions
with Boolean operators.
## Character Literals
Characters in Java are indices into the Unicode character set. They are 16-bit values that
can be converted into integers and manipulated with the integer operators, such as the
addition and subtraction operators. A literal character is represented inside a pair of single
quotes. All of the visible ASCII characters can be directly entered inside the quotes, such as
'
**a**
', '
**z**
', and '@'. For characters that are impossible to enter directly, there are several escape
sequences that allow you to enter the character you need, such as ' \' ' for the single-quote
n
character itself and ' \
' for the newline character. There is also a mechanism for directly
entering the value of a character in octal or hexadecimal. For octal notation, use the
backslash followed by the three-digit number. For example, ' \
**141**
' is the letter '
**a**
'. For
u
hexadecimal, you enter a backslash-u ( \
), then exactly four hexadecimal digits. For example,
' \
**u0061**
' is the ISO-Latin-1 '
**a**
' because the top byte is zero. ' \
**ua432**
' is a Japanese Katakana
character. Table 3-1 shows the character escape sequences.
## String Literals
String literals in Java are specified like they are in most other languages—by enclosing a
sequence of characters between a pair of double quotes. Examples of string literals are

---

<!-- Page 9 -->
44
PART I     The Java Language
|Escape Sequence|Description|
|---|---|
|\ddd|Octal character (ddd)|
|\uxxxx|Hexadecimal Unicode character (xxxx)|
|\'|Single quote|
|\"|Double quote|
|\\|Backslash|
|\r|Carriage return|
|\n|New line (also known as line feed)|
|\f|Form feed|
|\t|Tab|
|\b|Backspace|


Table 3-1
Character Escape Sequences
"Hello World"
"two\nlines"
" \"This is in quotes\""
The escape sequences and octal/hexadecimal notations that were defined for character
literals work the same way inside of string literals. One important thing to note about Java
strings is that they must begin and end on the same line. There is no line-continuation
escape sequence as there is in some other languages.
As you may know, in some other languages, including C/C++, strings are implemented as arrays of
NOTE
characters. However, this is not the case in Java. Strings are actually object types. As you will see later
in this book, because Java implements strings as objects, Java includes extensive string-handling
capabilities that are both powerful and easy to use.
# Variables
The variable is the basic unit of storage in a Java program. A variable is defined by the
combination of an identifier, a type, and an optional initializer. In addition, all variables have
a scope, which defines their visibility, and a lifetime. These elements are examined next.
## Declaring a Variable
In Java, all variables must be declared before they can be used. The basic form of a variable
declaration is shown here:
**type identifier**
[ =
**value**
][,
**identifier**
[=
**value**
] …];
Here,
**type**
is one of Java’s atomic types, or the name of a class or interface. (Class and
interface types are discussed later in Part I of this book.) The
**identifier**
is the name of the
variable. You can initialize the variable by specifying an equal sign and a value. Keep in
mind that the initialization expression must result in a value of the same (or compatible)

---

<!-- Page 10 -->
45
Chapter 3     Data Types, Variables, and Arrays
type as that specified for the variable. To declare more than one variable of the specified type,
use a comma-separated list.
Here are several examples of variable declarations of various types. Note that some
### Part I
include an initialization.
int a, b, c;            // declares three ints, a, b, and c.
int d = 3, e, f = 5;    // declares three more ints, initializing
// d and f.
byte z = 22;            // initializes z.
double pi = 3.14159;    // declares an approximation of pi.
char x = 'x';           // the variable x has the value 'x'.
The identifiers that you choose have nothing intrinsic in their names that indicates
their type. Java allows any properly formed identifier to have any declared type.
## Dynamic Initialization
Although the preceding examples have used only constants as initializers, Java allows
variables to be initialized dynamically, using any expression valid at the time the variable
is declared.
For example, here is a short program that computes the length of the hypotenuse of a
right triangle given the lengths of its two opposing sides:
// Demonstrate dynamic initialization.
class DynInit {
public static void main(String args[]) {
double a = 3.0, b = 4.0;
// c is dynamically initialized
double c = Math.sqrt(a * a + b * b);
System.out.println("Hypotenuse is " + c);
}
}
a
b
c
a
b
Here, three local variables—
,
, and
—are declared. The first two,
and
, are initialized
c
by constants. However,
is initialized dynamically to the length of the hypotenuse (using
sqrt( )
the Pythagorean theorem). The program uses another of Java’s built-in methods,
,
Math
which is a member of the
class, to compute the square root of its argument. The key
point here is that the initialization expression may use any element valid at the time of the
initialization, including calls to methods, other variables, or literals.
## The Scope and Lifetime of Variables
main( )
So far, all of the variables used have been declared at the start of the
method.
However, Java allows variables to be declared within any block. As explained in Chapter 2,
a block is begun with an opening curly brace and ended by a closing curly brace. A block
defines a
**scope**
. Thus, each time you start a new block, you are creating a new scope. A scope
determines what objects are visible to other parts of your program. It also determines the
lifetime of those objects.

---

<!-- Page 11 -->
46
PART I     The Java Language
Many other computer languages define two general categories of scopes: global and
local. However, these traditional scopes do not fit well with Java’s strict, object-oriented
model. While it is possible to create what amounts to being a global scope, it is by far the
exception, not the rule. In Java, the two major scopes are those defined by a class and those
defined by a method. Even this distinction is somewhat artificial. However, since the class
scope has several unique properties and attributes that do not apply to the scope defined
by a method, this distinction makes some sense. Because of the differences, a discussion of
class scope (and variables declared within it) is deferred until Chapter 6, when classes are
described. For now, we will only examine the scopes defined by or within a method.
The scope defined by a method begins with its opening curly brace. However, if that
method has parameters, they too are included within the method’s scope. Although this
book will look more closely at parameters in Chapter 6, for the sake of this discussion, they
work the same as any other method variable.
As a general rule, variables declared inside a scope are not visible (that is, accessible)
to code that is defined outside that scope. Thus, when you declare a variable within a
scope, you are localizing that variable and protecting it from unauthorized access and/or
modification. Indeed, the scope rules provide the foundation for encapsulation.
Scopes can be nested. For example, each time you create a block of code, you are
creating a new, nested scope. When this occurs, the outer scope encloses the inner scope.
This means that objects declared in the outer scope will be visible to code within the inner
scope. However, the reverse is not true. Objects declared within the inner scope will not be
visible outside it.
To understand the effect of nested scopes, consider the following program:
// Demonstrate block scope.
class Scope {
public static void main(String args[]) {
int x; // known to all code within main
x = 10;
if(x == 10) { // start new scope
int y = 20; // known only to this block
// x and y both known here.
System.out.println("x and y: " + x + " " + y);
x = y * 2;
}
// y = 100; // Error! y not known here
// x is still known here.
System.out.println("x is " + x);
}
}
x
main( )
As the comments indicate, the variable
is declared at the start of
’s scope and is
main( )
if
y
accessible to all subsequent code within
. Within the
block,
is declared. Since a
y
block defines a scope,
is only visible to other code within its block. This is why outside of
y = 100
its block, the line
; is commented out. If you remove the leading comment symbol,
y
if
a compile-time error will occur, because
is not visible outside of its block. Within the
x
block,
can be used because code within a block (that is, a nested scope) has access to
variables declared by an enclosing scope.

---

<!-- Page 12 -->
47
Chapter 3     Data Types, Variables, and Arrays
Within a block, variables can be declared at any point, but are valid only after they are
declared. Thus, if you define a variable at the start of a method, it is available to all of the
code within that method. Conversely, if you declare a variable at the end of a block, it is
### Part I
effectively useless, because no code will have access to it. For example, this fragment is
count
invalid because
cannot be used prior to its declaration:
// This fragment is wrong!
count = 100; // oops! cannot use count before it is declared!
int count;
Here is another important point to remember: variables are created when their scope is
entered, and destroyed when their scope is left. This means that a variable will not hold its
value once it has gone out of scope. Therefore, variables declared within a method will not
hold their values between calls to that method. Also, a variable declared within a block will
lose its value when the block is left. Thus, the lifetime of a variable is confined to its scope.
If a variable declaration includes an initializer, then that variable will be reinitialized
each time the block in which it is declared is entered. For example, consider the next
program:
// Demonstrate lifetime of a variable.
class LifeTime {
public static void main(String args[]) {
int x;
for(x = 0; x < 3; x++) {
int y = -1; // y is initialized each time block is entered
System.out.println("y is: " + y); // this always prints -1
y = 100;
System.out.println("y is now: " + y);
}
}
}
The output generated by this program is shown here:
y is: -1
y is now: 100
y is: -1
y is now: 100
y is: -1
y is now: 100
y
for
As you can see,
is reinitialized to –1 each time the inner
loop is entered. Even though
it is subsequently assigned the value 100, this value is lost.
One last point: Although blocks can be nested, you cannot declare a variable to have
the same name as one in an outer scope. For example, the following program is illegal:
// This program will not compile
class ScopeErr {
public static void main(String args[]) {
int bar = 1;

---

<!-- Page 13 -->
48
PART I     The Java Language
{               // creates a new scope
int bar = 2;  // Compile-time error – bar already defined!
}
}
}
# Type Conversion and Casting
If you have previous programming experience, then you already know that it is fairly common
to assign a value of one type to a variable of another type. If the two types are compatible,
then Java will perform the conversion automatically. For example, it is always possible to
int
long
assign an
value to a
variable. However, not all types are compatible, and thus, not
all type conversions are implicitly allowed. For instance, there is no automatic conversion
double
byte
defined from
to
. Fortunately, it is still possible to obtain a conversion between
incompatible types. To do so, you must use a
**cast**
, which performs an explicit conversion
between incompatible types. Let’s look at both automatic type conversions and casting.
## Java’s Automatic Conversions
When one type of data is assigned to another type of variable, an
**automatic type conversion**
will take place if the following two conditions are met:
• The two types are compatible.
• The destination type is larger than the source type.
When these two conditions are met, a
**widening conversion**
takes place. For example, the
int
byte
type is always large enough to hold all valid
values, so no explicit cast statement is
required.
For widening conversions, the numeric types, including integer and floating-point types,
are compatible with each other. However, there are no automatic conversions from the
char
boolean
char
boolean
numeric types to
or
. Also,
and
are not compatible with each other.
As mentioned earlier, Java also performs an automatic type conversion when storing a
byte
short
long
char
literal integer constant into variables of type
,
,
, or
.
## Casting Incompatible Types
Although the automatic type conversions are helpful, they will not fulfill all needs. For
int
byte
example, what if you want to assign an
value to a
variable? This conversion will not
byte
int
be performed automatically, because a
is smaller than an
. This kind of conversion
is sometimes called a
**narrowing conversion**
, since you are explicitly making the value narrower
so that it will fit into the target type.
To create a conversion between two incompatible types, you must use a cast. A
**cast**
is
simply an explicit type conversion. It has this general form:
(
**target**
-
**type**
)
**value**

---

<!-- Page 14 -->
49
Chapter 3     Data Types, Variables, and Arrays
Here,
**target-type**
specifies the desired type to convert the specified value to. For example, the
int
byte
following fragment casts an
to a
. If the integer’s value is larger than the range of a
byte
byte
, it will be reduced modulo (the remainder of an integer division by the)
’s range.
### Part I
int a;
byte b;
// …
b = (byte) a;
A different type of conversion will occur when a floating-point value is assigned to an
integer type:
**truncation**
. As you know, integers do not have fractional components. Thus,
when a floating-point value is assigned to an integer type, the fractional component is lost.
For example, if the value 1.23 is assigned to an integer, the resulting value will simply be 1.
The 0.23 will have been truncated. Of course, if the size of the whole number component is
too large to fit into the target integer type, then that value will be reduced modulo the
target type’s range.
The following program demonstrates some type conversions that require casts:
// Demonstrate casts.
class Conversion {
public static void main(String args[]) {
byte b;
int i = 257;
double d = 323.142;
System.out.println("\nConversion of int to byte.");
b = (byte) i;
System.out.println("i and b " + i + " " + b);
System.out.println("\nConversion of double to int.");
i = (int) d;
System.out.println("d and i " + d + " " + i);
System.out.println("\nConversion of double to byte.");
b = (byte) d;
System.out.println("d and b " + d + " " + b);
}
}
This program generates the following output:
Conversion of int to byte.
i and b 257 1
Conversion of double to int.
d and i 323.142 323
Conversion of double to byte.
d and b 323.142 67
byte
Let’s look at each conversion. When the value 257 is cast into a
variable, the result is the
byte
remainder of the division of 257 by 256 (the range of a
), which is 1 in this case. When

---

<!-- Page 15 -->
50
PART I     The Java Language
d
int
d
byte
the
is converted to an
, its fractional component is lost. When
is converted to a
, its
fractional component is lost,
**and**
the value is reduced modulo 256, which in this case is 67.
# Automatic Type Promotion in Expressions
In addition to assignments, there is another place where certain type conversions may
occur: in expressions. To see why, consider the following. In an expression, the precision
required of an intermediate value will sometimes exceed the range of either operand. For
example, examine the following expression:
byte a = 40;
byte b = 50;
byte c = 100;
int d = a * b / c;
a * b
byte
The result of the intermediate term
easily exceeds the range of either of its
byte
short
operands. To handle this kind of problem, Java automatically promotes each
,
,
char
int
or
operand to
when evaluating an expression. This means that the subexpression
a*b
is performed using integers—not bytes. Thus, 2,000, the result of the intermediate
50 * 40
a
b
byte
expression,
, is legal even though
and
are both specified as type
.
As useful as the automatic promotions are, they can cause confusing compile-time
errors. For example, this seemingly correct code causes a problem:
byte b = 50;
b = b * 2; // Error! Cannot assign an int to a byte!
byte
byte
The code is attempting to store 50 * 2, a perfectly valid
value, back into a
int
variable. However, because the operands were automatically promoted to
when the
int
expression was evaluated, the result has also been promoted to
. Thus, the result of the
int
byte
expression is now of type
, which cannot be assigned to a
without the use of a cast.
This is true even if, as in this particular case, the value being assigned would still fit in the
target type.
In cases where you understand the consequences of overflow, you should use an explicit
cast, such as
byte b = 50;
b = (byte)(b * 2);
which yields the correct value of 100.
## The Type Promotion Rules
Java defines several
**type promotion**
rules that apply to expressions. They are as follows: First,
byte
short
char
int
all
,
, and
values are promoted to
, as just described. Then, if one operand
long
long
float
is a
, the whole expression is promoted to
. If one operand is a
, the entire
float
double
double
expression is promoted to
. If any of the operands are
, the result is
.
The following program demonstrates how each value in the expression gets promoted
to match the second argument to each binary operator:

---

<!-- Page 16 -->
51
Chapter 3     Data Types, Variables, and Arrays
class Promote {
public static void main(String args[]) {
byte b = 42;
### Part I
char c = 'a';
short s = 1024;
int i = 50000;
float f = 5.67f;
double d = .1234;
double result = (f * b) + (i / c) - (d * s);
System.out.println((f * b) + " + " + (i / c) + " - " + (d * s));
System.out.println("result = " + result);
}
}
Let’s look closely at the type promotions that occur in this line from the program:
double result = (f * b) + (i / c) - (d * s);
f * b, b
float
In the first subexpression,
is promoted to a
and the result of the subexpression
float
i/c, c
int
int
is
. Next, in the subexpression
is promoted to
, and the result is of type
.
d * s
s
double
Then, in
, the value of
is promoted to
, and the type of the subexpression is
double
float
int
double
. Finally, these three intermediate values,
,
, and
, are considered. The
float
int
float
float
double
outcome of
plus an
is a
. Then the resultant
minus the last
is
double
promoted to
, which is the type for the final result of the expression.
# Arrays
An
**array**
is a group of like-typed variables that are referred to by a common name. Arrays of
any type can be created and may have one or more dimensions. A specific element in an
array is accessed by its index. Arrays offer a convenient means of grouping related
information.
If you are familiar with C/C++, be careful. Arrays in Java work differently than they do in those
NOTE
languages.
## One-Dimensional Arrays
A
**one-dimensional array**
is, essentially, a list of like-typed variables. To create an array, you first
must create an array variable of the desired type. The general form of a one-dimensional
array declaration is
**type var-name**
[ ];
Here,
**type**
declares the element type (also called the base type) of the array. The element type
determines the data type of each element that comprises the array. Thus, the element
type for the array determines what type of data the array will hold. For example, the
month_days
following declares an array named
with the type “array of int”:
int month_days[];

---

<!-- Page 17 -->
52
PART I     The Java Language
month_days
Although this declaration establishes the fact that
is an array variable, no
month_days
array actually exists. To link
with an actual, physical array of integers, you must
new
month_days
new
allocate one using
and assign it to
.
is a special operator that allocates
memory.
new
You will look more closely at
in a later chapter, but you need to use it now to
new
allocate memory for arrays. The general form of
as it applies to one-dimensional
arrays appears as follows:
**array-var**
= new
**type**
[
**size**
];
Here,
**type**
specifies the type of data being allocated,
**size**
specifies the number of elements in
new
the array, and
**array-var**
is the array variable that is linked to the array. That is, to use
to
allocate an array, you must specify the type and number of elements to allocate. The elements
new
false
in the array allocated by
will automatically be initialized to zero (for numeric types),
boolean
null
(for
), or
(for reference types, which are described in a later chapter). This
month_days
example allocates a 12-element array of integers and links them to
:
month_days = new int[12];
month_days
After this statement executes,
will refer to an array of 12 integers. Further, all
elements in the array will be initialized to zero.
Let’s review: Obtaining an array is a two-step process. First, you must declare a variable
of the desired array type. Second, you must allocate the memory that will hold the array,
new
using
, and assign it to the array variable. Thus, in Java all arrays are dynamically
allocated. If the concept of dynamic allocation is unfamiliar to you, don’t worry. It will
be described at length later in this book.
Once you have allocated an array, you can access a specific element in the array by
specifying its index within square brackets. All array indexes start at zero. For example,
month_days
this statement assigns the value 28 to the second element of
:
month_days[1] = 28;
The next line displays the value stored at index 3:
System.out.println(month_days[3]);
Putting together all the pieces, here is a program that creates an array of the number of
days in each month:
// Demonstrate a one-dimensional array.
class Array {
public static void main(String args[]) {
int month_days[];
month_days = new int[12];
month_days[0] = 31;
month_days[1] = 28;
month_days[2] = 31;
month_days[3] = 30;
month_days[4] = 31;
month_days[5] = 30;

---

<!-- Page 18 -->
53
Chapter 3     Data Types, Variables, and Arrays
month_days[6] = 31;
month_days[7] = 31;
month_days[8] = 30;
### Part I
month_days[9] = 31;
month_days[10] = 30;
month_days[11] = 31;
System.out.println("April has " + month_days[3] + " days.");
}
}
When you run this program, it prints the number of days in April. As mentioned, Java array
month_days[3]
indexes start with zero, so the number of days in April is
or 30.
It is possible to combine the declaration of the array variable with the allocation of the
array itself, as shown here:
int month_days[] = new int[12];
This is the way that you will normally see it done in professionally written Java programs.
Arrays can be initialized when they are declared. The process is much the same as that
used to initialize the simple types. An
**array initializer**
is a list of comma-separated expressions
surrounded by curly braces. The commas separate the values of the array elements. The
array will automatically be created large enough to hold the number of elements you specify
new
in the array initializer. There is no need to use
. For example, to store the number of
days in each month, the following code creates an initialized array of integers:
// An improved version of the previous program.
class AutoArray {
public static void main(String args[]) {
int month_days[] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31,
30, 31 };
System.out.println("April has " + month_days[3] + " days.");
}
}
When you run this program, you see the same output as that generated by the previous
version.
Java strictly checks to make sure you do not accidentally try to store or reference values
outside of the range of the array. The Java run-time system will check to be sure that all
array indexes are in the correct range. For example, the run-time system will check the
month_days
value of each index into
to make sure that it is between 0 and 11 inclusive. If
you try to access elements outside the range of the array (negative numbers or numbers
greater than the length of the array), you will cause a run-time error.
Here is one more example that uses a one-dimensional array. It finds the average of a
set of numbers.
// Average an array of values.
class Average {
public static void main(String args[]) {
double nums[] = {10.1, 11.2, 12.3, 13.4, 14.5};
double result = 0;
int i;

---

<!-- Page 19 -->
54
PART I     The Java Language
for(i=0; i<5; i++)
result = result + nums[i];
System.out.println("Average is " + result / 5);
}
}
## Multidimensional Arrays
In Java,
**multidimensional arrays**
are actually arrays of arrays. These, as you might expect, look
and act like regular multidimensional arrays. However, as you will see, there are a couple
of subtle differences. To declare a multidimensional array variable, specify each additional
index using another set of square brackets. For example, the following declares a two-
twoD
dimensional array variable called
:
int twoD[][] = new int[4][5];
twoD
This allocates a 4 by 5 array and assigns it to
. Internally, this matrix is implemented as
int
an
**array**
of
**arrays**
of
. Conceptually, this array will look like the one shown in Figure 3-1.
The following program numbers each element in the array from left to right, top to
bottom, and then displays these values:
// Demonstrate a two-dimensional array.
class TwoDArray {
public static void main(String args[]) {
int twoD[][]= new int[4][5];
int i, j, k = 0;
for(i=0; i<4; i++)
for(j=0; j<5; j++) {
twoD[i][j] = k;
k++;
}
for(i=0; i<4; i++) {
for(j=0; j<5; j++)
System.out.print(twoD[i][j] + " ");
System.out.println();
}
}
}
This program generates the following output:
0 1 2 3 4
5 6 7 8 9
10 11 12 13 14
15 16 17 18 19
When you allocate memory for a multidimensional array, you need only specify the
memory for the first (leftmost) dimension. You can allocate the remaining dimensions

---

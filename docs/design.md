# Emerald Programming Language Design

Emerald is a small toy language designed for the purpose of teaching how to make a compiler

It is designed to resemble that of javascript because of how familiar it is.

## Features

### Variables
```javascript
var name = "Alex"
const width = 1080

width = 920 //This will not compile
name = "John" //This will compile
```

### Functions
```javascript
const factorial = function(n: int) -> int{
    if(n == 0 || n == 1) return n
    return n * (factorial(n - 1))
}

const factResult = factorial(5) //This should be 120
```

### Data structures
```javascript
import std.debug.print

const Person = data(name: string, age: int){
    const speak = function(self: Self){
        print("Hello, my name is " + self.name + " and I am " + self.age + " years old!")
    }
}

john = Person("John", 32)
john.speak() //Hello, my name is John and I am 32 years old!
```

### References
```javascript
import std.debug.print

//Declare age as pub so we can call it externally
const Person = data(name: string, pub age: int){
    pub const birthday = function(self: $Ref){
        self.age += 1
    }
}

john = Person("John", 32)
john.birthday()

johnRef = $john //Reference to john
//Dereference johnRef and get 'age' field
print(*johnRef.age.str()) //33
```

### Link Libraries
```javascript
//main.em
import std.debug.print

pub extern const CreateHelloWorld = function() -> string

const helloWorld = CreateHelloWorld()
print(helloWorld)
```
```c
//CreateHelloWorld.c
char** CreateHelloWorld(){
    return "Hello, world!";
}
```
```
gcc CreateHelloWorld.c HelloWorld.o
ar rcs HelloWorld.a HelloWorld.o
emerald main.em -link HelloWorld.so
```

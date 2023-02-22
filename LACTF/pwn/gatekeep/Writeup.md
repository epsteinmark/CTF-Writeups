gatekeep.c will be referenced within the writeup and is provided within CTF-Writeups/LACTF/pwn/gatekeep/gatekeep.c

## Challenge Description
If I gaslight you enough, you won't be able to get my flag! :) 
a netcat host and port was provided to interact with the challenge
gatekeep.c was provided
a Dockerfile was provided

## Difficulty
529 solves / 138 points

## Solution
### int main()
Upon downloading the file gatekeep.c, I opened it and inspected the main function. I immediately saw the command `setbuf(stdout, NULL);` I looked up the command and through [Tutorials Point](https://www.tutorialspoint.com/c_standard_library/c_function_setbuf.htm) which revealed that the stream of stdout is null. That clearly implied that we needed a buffer overflow of some kind, so I continued searching with that in mind. The main function then calls the function check() so I move to that function

### int check()
Check immediately declares three variables:
```
char input[15];
char pass[10];
int access = 0;
```
Continuing the search through the function, the function `print_flag()` is called under `if(access)` which is clearly what I wanted. An integer returns true if it is anything other than 0, so I knew I needed to buffer overflow it. Therefore, when `gets(input);` gets called, I had to buffer overflow to access, which I accomplished by writing 26 a's. The first 15 a's fill input, the next 10 a's fill pass, and the final a gets converted into an int through ascii which sets access equal to 65. When `if(access)` runs as `if(65)` it returns true and prints the flag.

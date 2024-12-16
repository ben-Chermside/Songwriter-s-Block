# ABC Encoder Spec

The following is an agreed-upon conversion of ABC file to integer token stream
so that development of ML model and the encoder implementation itself can occur
simultaneously. 

The first three tokens in any token stream will be the following:
- Song type
- Time signature
- Default beat unit
- Mode

The body of the token stream will consist of the following types of tokens:
- Note (two sequential tokens describing pitch and then rhythm)
- Rest: an unaccompanied rhythm token will be interpreted as a rest
- Barline
- Start repeat
- End repeat
- beginnings of numbered endings

## Notes
### Pitch
0-11: transposed as `[C-B]`  
12-23: transposed as `[c-b]`  
24-35: transposed as `[C,-B,]`  
36-47: transposed as `[c'-b']`

### Rhythm (and Rests)
All values in reference to default duration specified  
48: 1/1  
49: 1/2  
50: 2/1  
51: 3/1  
52: 1/3  
53: 1/4  
54: 2/3  
55: 3/2  
56: 4/1  
57: 5/1  
58: 1/5  
59: 1/6  
60: 2/5  
61: 3/4  
62: 4/3  
63: 5/2  
64: 6/1  
...  
We will reserve values up to (not including) 128 as needed to extend this pattern out.  
Pattern is when one of $a$ or $b$ in $a / b$ is 1, increase the other value by one. Otherwise, alternate
removing from $a$ and adding to $b$ and vice versa. Only use value when $a$ and $b$ are coprime.
If wanted, we can write a script to print out all possible values in this or a similar pattern.

## Special Music Tokens
128: Barline `|`  
129: Start Repeat `|:`  
130: End Repeat `:|`  
131-139: Start of numbered endings 1-9  

Space up to (not including) 256 is reserved for future special music tokens.

## Special Metadata tokens

My solution to this was a little scuffed but we got there in the end.

I went to the website and realized very quickly that the goal was to hit the button. Obviously the button moves.

First, I tried to open a console, which failed due to the nature of the challenge. Instead, you can use
view-source:https://terms-and-conditions.chall.lac.tf (it doesn't work anymore) but it did then. This 
revealed an analytics.js file. This revealed some obfuscated Javascript. To deobfuscate it, I used https://deobfuscate.io/ which took me to https://obf-io.deobfuscate.io/.

When I looked at the code, I saw 
```javascript
alert("ob`wexwkbw\\avwwlm\\tbp\\gfejmjwfoz\\mlw\\lmf\\le\\wkf\\wfqnp~".split``.map(_0x286792 => String.fromCharCode(_0x286792.charCodeAt(0) ^ 3)).join``);
```

I ran this in a chrome console and got lactf{that_button_was_definitely_not_one_of_the_terms}.


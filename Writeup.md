There is an associated pcap that I probably deleted.

## Deadface CTF 2023

## Challenge Description 
One of our teammates at Turbo Tactical ran a phishing campaign on spookyboi and thinks spookyboi may have submitted credentials. We need you to take a look at the PCAP and see if you can find the credentials.

## Difficulty
Very easy

## Solution
One way is to note that the username is given to us, and so we can just search by it using something like `frame contains “spookyboi”`. This is a very clean way of doing it I found in a writeup. Another way (the way I did it) is to note that the name is Git Rekt, and a phishing campaign naturally implies an HTTP post so you can apply a `http` filter and just find the POST or use `http.request.method == "POST"` to see it directly. Then the flag becomes obvious.

flag{SpectralSecrets#2023}
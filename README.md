# Tech Challange Scam

I've recently done a tech challenge which had a suspicious piece of code in it.
Shortly after finding this I asked them about it and had my question removed and I was blocked by the dev that was managing it.
It became clear that it was a scam and I had to go a bit deeper into what was happening and what they were trying to do.
You can find the [script](./script.js) and run it through Docker (for safety) with:
```
$ docker build -t <IMAGE_NAME> .
$ docker run --rm -it --name <CONTAINER_NAME> --cap-drop=ALL <IMAGE_NAME>
```

I've also left how it was hidden on the file [here](./hidden-script.js) so you can also see how they usually do it.
Luckily when I've opened this file the line simply wrapped which allowed me to see it with ease but looking through
github you can see that the symbols are detected as well.

After running the script on an isolated environment, I've noticed two IPs at the same port that are being used by the script:

- 216.173.115.200:1244
- 67.203.7.209:1244

Along with the order of requests:

![](wireshark-requests.png?raw=true)

The first IP seems to be used to fetch some sort of key and the second one actually downloads the actual malicious payload at the home directory and it does in a cunning way to try to avoid the target from noticing it:

- [~/.vscode](./payloads/.vscode)
- [~/.npl](./payloads/.npl)

That `.npl` payload is actually encoded in multiple rounds using base64 and in the end the script that is formed is at [npl-final.py](./payloads/npl-final.py). The [decode-recursive.py](./payloads/decode-recursive.py) is just an util script that was used to decode the base64 payload until it actually gets to the final script.

The vscode folder contents are downloaded from the decoded `.npl` script. Inside .vscode, there's another obfuscated script which seems to be the one that keeps running (there's a `setInterval`) there. Potentially it's the script that actually tries to gather and send information to the mentioned IP addresses.

![](processes.png?raw=true)

Regardless, after running the script with `strace -f -o trace.log node script.js` within the container I could detect on [trace.log](./trace.log) the IPs mentioned and the files that it tries to open and I believe which are sent to 67.203.7.209:1244

```
23    openat(AT_FDCWD, "/etc/passwd", O_RDONLY|O_CLOEXEC) = 21
43    faccessat(AT_FDCWD, "/root/.config/Exodus/exodus.wallet", F_OK) = -1 ENOENT (No such file or directory)
43    faccessat(AT_FDCWD, "/root/.config/atomic/Local Storage/leveldb", F_OK) = -1 ENOENT (No such file or directory)
43    faccessat(AT_FDCWD, "/root/.config/google-chrome", F_OK) = -1 ENOENT (No such file or directory)
43    faccessat(AT_FDCWD, "/root/.config/BraveSoftware/Brave-Browser", F_OK) = -1 ENOENT (No such file or directory)
43    faccessat(AT_FDCWD, "/root/.config/opera", F_OK) = -1 ENOENT (No such file or directory)
43    faccessat(AT_FDCWD, "/root/.local/share/keyrings/", F_OK) = -1 ENOENT (No such file or directory)
43    faccessat(AT_FDCWD, "/root/.config/google-chrome", F_OK) = -1 ENOENT (No such file or directory)
43    faccessat(AT_FDCWD, "/root/.mozilla/firefox/", F_OK) = -1 ENOENT (No such file or directory)
```

I'm still unsure if it might be doing anything else but seems like that was the malware does in general.
Their attack model would be that the target would be reloading the project while working on it which would simply
rerun the script over and over again.

I'm opening this for others to see at least one of their strategies for fooling people and also to remember to run whatever external
code on an isolated environment, sometimes even Docker will not suffice and going with an external VM might be necessary. Also, trust your instincts because once I found that, I figure it could be part of the test (although I had a strong feeling it wasn't) but after how their dev handled my question, there was no doubt.

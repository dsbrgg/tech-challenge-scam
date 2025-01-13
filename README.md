# Tech Challange Scam

I've recently done a tech challenge which had a suspicious piece of code in it.
Shortly after finding this I asked them about it and had my question removed and I was blocked by the dev that was managing it.
It became clear that it was a scam and I had to go a bit deeper into what was happening and what they were trying to do.

I ended up getting contacted by multiple of these and they all have the same approach. I'll leave the details on each folder for each scam company.

## TechVantage

You can find the [script](./tech-vantage/script.js) and run it through Docker (for safety) with:
```
$ docker build -t <IMAGE_NAME> .
$ docker run --rm -it --name <CONTAINER_NAME> --cap-drop=ALL <IMAGE_NAME>
```

I've also left how it was hidden on the file [here](./tech-vantage/hidden-script.js) so you can also see how they usually do it.
Luckily when I've opened this file the line simply wrapped which allowed me to see it with ease but looking through
github you can see that the symbols are detected as well.

After running the script on an isolated environment, I've noticed two IPs at the same port that are being used by the script:

- 216.173.115.200:1244
- 67.203.7.209:1244

Along with the order of requests:

![](./tech-vantage/wireshark-requests.png?raw=true)

The first IP seems to be used to fetch some sort of key and the second one actually downloads the actual malicious payload at the home directory and it does in a cunning way to try to avoid the target from noticing it:

- [~/.vscode](./tech-vantage/payloads/.vscode)
- [~/.npl](./tech-vantage/payloads/.npl)

That `.npl` payload is actually encoded in multiple rounds using base64 and in the end the script that is formed is at [npl-final.py](./tech-vantage/payloads/npl-final.py). The [decode-recursive.py](./tech-vantage/payloads/decode-recursive.py) is just an util script that was used to decode the base64 payload until it actually gets to the final script.

The vscode folder contents are downloaded from the decoded `.npl` script. Inside .vscode, there's another obfuscated script which seems to be the one that keeps running (there's a `setInterval`) there. Potentially it's the script that actually tries to gather and send information to the mentioned IP addresses.

![](./tech-vantageprocesses.png?raw=true)

Regardless, after running the script with `strace -f -o trace.log node script.js` within the container I could detect on [trace.log](./tech-vantage/trace.log) the IPs mentioned and the files that it tries to open and I believe which are sent to 67.203.7.209:1244

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

The name of the company is TechVantage (https://www.linkedin.com/company/techvantagetm/) and even after reporting it (and asking other people to do so as well) it's still up there.

## Cryptolope

Another one came to me and the procedure is always the same:

- Provide some bogus context
- Send a repo (usually bitbucket)
- Wait for you to run the project

It's common for them to tell you that the project is about frontend/backend specifically so you don't look at a certain piece of code.
Here's the [source code](https://bitbucket.org/cryptolope/token-locator/src/main/) (if it's still avaiable).

You can check the section that is heavily obfuscated [here](./cryptolope/search.min.js) and the payload is downloaded at the home directory in [.sysinfo](./cryptolope/.sysinfo).
I have the impression they might all get these scripts from the same location as their implementation is also the same:

- Download the malware from an obfuscated script
- It's a python script which decompresses a string and base64 decodes it multiple times (50+)
- The python script downloads the actual malware into another folder that would seem harmless but it's out of place (.sysinfo in Darwin arch, .vscode at home folder, etc...)

Best of luck for this one though as it's script (if you use my [decode](./tech-vantage/payloads/decode-recursive.py) to test it out) was incorrectly encoded in a round and it won't reach the final script in the end.

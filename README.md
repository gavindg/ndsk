## ndsk (何だその漢字 -- what's that kanji?)

 A console app for Japanese learners that quickly scrapes the web for information on unfamiliar kanji and vocab words.
 ndsk scrapes the Japanese dictionary website [jisho.org](https://jisho.org) for information. As of now, ndsk is only capable of saving you a few clicks when you need to quickly look up the readings of a kanji, but later down the line it will be capable of quickly getting definitions of vocabulary and more, giving the user a high level of control over the format of the output as well.

#### Note: this project is currently in its very early stages.

 I plan to continuously update it over time. As of right now, it offers the following (very limited) features:
 
* Display the On'yomi readings of a single Kanji.
* Display the Kun'yomi readings of a single Kanji.
* (To a small degree) format the output of the above two commands.

## Usage

`ndsk [Kanji] [flags...]`

##### Flags
* `-k` -- Lists the Kun'yomi readings of the given `Kanji`
* `-o` -- Lists the On'yomi readings of the given `Kanji`

Example: get the Kun'yomi and On'yomi readings of '日'

`ndsk 日 -k -o`

Output:

```
Kun: ひ, -び, -か
On: ニチ, ジツ
```

Notes: 

* Output is ordered in the order of the flags, so `ndsk 日 -o -k` would print the above results with On'yomi readings first and Kun'yomi second.
* Currently, `ndsk [Kanji]` (no flags) is an alias for `ndsk [Kanji] -k -o`


## The Future

 This little console app is just the beginning of a much bigger idea of mine. Some future plans outside of obvious features (such as pulling meanings for vocab words) include:

* Adding a GUI

>(I chose python because it's cross-platform, but the app probably won't be useful to people outside of "MacOS/Linux console wizard Japanese learners" group until there's a GUI...)

* Creating a Arc (Ok... chromium) browser extension

>(My dream for this project is to be able to be able to highlight a kanji in my browser and get a little pop-up window above it that tells me its meaning/reading, in place without needing any new tab, window, or application open. This entails a full JavaScript rewrite. I frankly don't have enough JS experience to make this happen for now, but it will happen, eventually!)

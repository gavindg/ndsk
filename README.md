## ndsk (何だその漢字 -- what's that kanji?)

 A console app for Japanese learners that quickly scrapes the web for information on unfamiliar kanji and vocab words.
 NDSK scrapes the japanese dictionary website [jisho.org](https://jisho.org) for information. As of now, ndsk is only capable of saving you a few clicks when you need to quickly look up the readings of a kanji, but later down the line it will be capable of quickly getting definitions of vocabulary and more, giving the user a high level of control over the format of the output as well.

#### Note: this project is currently in its very early stages.

 I plan to continuously update it over time. As of right now, it offers the following (very limited) features:
 
* Display the On'yomi readings of a single Kanji.
* Display the Kun'yomi readings of a single Kanji.
* (To a small degree) format the output of the above two commands.

#### Usage

`ndkk [Kanji] [flags...]`

##### Flags
* `-k` -- Lists the Kun'yomi readings of the given `Kanji`
* `-o` -- Lists the On'yomi readings of the given `Kanji`

Example: get the Kun'yomi and On'yomi readings of '日'

`ndkk 日 -k -o`

Output:

```
Kun: ひ, -び, -か
On: ニチ, ジツ
```

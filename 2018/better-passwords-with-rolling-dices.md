---
title: "Better passwords with rolling dices"
date: "2018-11-03"
categories: 
  - "security"
---

In this post I will share my thoughts on passwords strength and will share a small project I did for this topic :)

Everybody understands significance of passwords in everyday life. With, or without password managers, everybody needs to remember bunch of passwords.

In this post I will focus only on randomness aspect of the passwords, it is not a complete guide on safe management, generation and usage of passwords.

While annoying to remember, they are important for our safety. Generating good (random) passwords is quite hard, so people usually end up with hard-to-remember, but easy-to-guess passwords :). When talking about passwords from this perspective it seems that the XKCD citation is mandatory: [here it is](https://xkcd.com/936/).

 

## Randomness

 

People usually think that the longer the password is the safer it is. It is however important to realize that it is true only as long as all the words/characters in it are chosen **truly randomly**. So relying on human feeling of randomness won't help us and is very deceiving - randomly pressing keys on your keyboard will result in hard-to-remember password with increased probability of letters in some areas of the keyboard. Trying to "randomly" come up with six words will probably result in words which have increased probability of being chosen - based on your background, social situation, job, etc.

 

## Dice

 

Here comes to the rescue a simple device for generating fairly good randomness - die. If you neglect material, density and shape imperfections (and hide the dice on a very secret place afterwards :) ) then you can conclude, that you get fairly random choices.

So you can use dice to help you with choosing a random letters, or random words. Passphrases consisting of random words are usually easier to remember, so we will go with it.

 

## Diceware

 

Using rolling dice is exactly the idea behind **Diceware** - a technique for random selection of words from a wordlist. How it works is nicely explained on [those pages](http://world.std.com/~reinhold/diceware.html), [faq](http://world.std.com/~reinhold/dicewarefaq.html).

In a nutshell it works like this: each word has assigned a unique key, which consists of a let's say 5 dice rolls. For example _21116 - cling._ So a wordlist of 5 dice rolls has 7 776 words - all possible combinations of a 5 random dice rolls (6^5). 5 dice rolls will give you one random word, do this 6 times for six words and you have a decent passphrase.

 

## Entropy

 

It is good to know the strength or entropy of your password. Entropy is a complex topic and depends on many factors. But assuming that your password consists of truly random elements, you can calculate its entropy based on all possible combinations. Note that entropy depends on knowledge of the technique that was used to generate the password.

### Random letter passwords

If choosing 8 random letters from [base64](https://en.wikipedia.org/wiki/Base64) character set, each letter gives you 6 bits of entropy resulting in total 48 bits of entropy. One randomly chosen element (one character in this case) gives you log2(N) bits of entropy, where N is total amount of possible choices. Notice that one character can give you 6 bits of entropy in this case only.

### Random word passphrases

If choosing 8 random words from 7 776 words wordlist, each word gives you approx. 12.92 bit of entropy: log2(7 776). So using 4 random words will give you more security/entropy than using 8 random letters - 51.7 bits. Remembering 4 random words is definitely easier.

Official Diceware wordlist is built with 7 776 words. However we can increase the strength of the wordlist by adding more words into it. If we rolled the dice 6 times instead of 5 times, we would get 46 656 words long wordlist with approx. 15.51 bits of entropy per word. So by keeping the amount of words - 4 while increasing the wordlist will increase our entropy to 62.04 bits. Without any effort on remembering. This is analogous to increasing character set in random letter passwords - adding special characters, numbers, symbols etc.

You might be thinking - shouldn't my wordlist be secret? Not really, this is not how you can confidently increase your password strength. Knowing the wordlist (in passphrase attacks) is the same as knowing the alphabet (in random letter password attacks).

 

## My take on it

 

So now I can get to the "my small project" part.

I generated a couple [of wordlists in Slovak language](https://github.com/jtomori/diceware_slovak). They have enough words for 5, 6, 7 and 8 dice rolls with 7 776, 46 656, 279 936 and 1 679 616 words respectively. This means that you can choose the strongest wordlist and start rolling your safe pass phrases. For the reference I also included calculations and an entropy table for different passphrases lengths and wordlists.

Generation is done in _Python_ and you can easily take it and generate it for your language :)

Slovak wordlist is based on [this source](https://p.brm.sk/sk_wordlist/). The nice thing is that is is sorted by usage frequency, so the smaller wordlists will not get uncommon words.

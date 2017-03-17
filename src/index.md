
$add_style(page.css)

$write_header

$begin_content

!<[avatar](/img/home/avatar.png)

Hello! I'm Gabriel Francisco Mandaji (aka, GFM) a software developer and
hobbyist game developer.

I used to play around with RPG Maker and Flash (ActionScript 3 + Flixel), but
nowadays, except for the occasional Python script (like this site), most of my
projects are written in C. Reinventing the wheel is fun and great for learning!

For now, this page is mostly a portfolio with the game I've made. Eventually, I
plan to also start to write blog posts directly here.

# Current projects

## JJAT 1.5

Enhanced version of JJAT. Play with a friend or control two characters at once
on this action platformer.

Different from the original game, each character will have a distinct role.
"Swordy" can attack enemies, is quicker and has double jump. "Gunny" is way less
agile but has a teleport gun, which actually switch the character and the
targeted entity.

## GFraMe

My personal framework for making games. It's SDL2 based and has features to
allow instanced drawing (i.e., it may handle thousands of sprites at 120 FPS)
and easily rebindable controls. It's also integrated with my synthesizer, so
songs are usually simple text files (which requires way less storage than
sound files).

It's always being enhanced, and the next planned refactor should enable
supporting older platforms (e.g.,  Mega Drive/Sega Genesis through
[GENDEV](https://github.com/kubilus1/gendev)). I don't know when this new
version will be started, though...

## c_synth

Synthesizes MML-like songs into waveforms. It uses a custom language that was
never properly documented...

An enhanced version has been started but is currently stopped. It will have
proper documentation, use a fixed amount of memory and synthesize songs on
runtime, allowing some effects to be applied to a song or to its tracks
separately.

$end_content



$add_game(ggj, src/game/ggj/ggj16.json)
$add_game(ggj, src/game/ggj/ggj15.json)
$add_game(ggj, src/game/ggj/ggj14.json)

$add_game(1gam, src/game/1gam/2013-03-dragonrush.json)
$add_game(1gam, src/game/1gam/2013-02-shooter.json)
$add_game(1gam, src/game/1gam/2013-01-colorrunner.json)

$add_game(campjam, src/game/campjam/campjam16.json)
$add_game(campjam, src/game/campjam/campjam15.json)
$add_game(campjam, src/game/campjam/campjam14.json)

$add_game(others, src/game/otherjam/001_cow.json)

$add_style(page.css)
$add_style(icon.css)
$add_style(game_description.css)

$add_script(mouseover.js)
$add_script(game_description.js)

$write_header

$begin_content

# Other Jams

List of games I've made for various other jams.

## Global Game Jam

The [Global Game Jam](http://globalgamejam.org/) is an annual game jam that
takes places in various jam sites through the world. It's usually held at the
end of January. It's currently a 48 hours event

$insert_game_list(ggj)

## One Game a Month

[One Game a Month](http://www.onegameamonth.com/) is a monthly challenge to try
and finish one game each month for a whole year.

$insert_game_list(1gam)

## CampJam

The CampJam is a local 48 hours game jam that (usually) takes place the weekend
before classes are back, on the July vacations.

$insert_game_list(campjam)

## Others

This category has games from jams that I have only taken part a few times, so
there was no reason to create a separated category for them.

$insert_game_list(others)

$end_content


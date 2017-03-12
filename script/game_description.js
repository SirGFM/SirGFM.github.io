/**
 * @file script/game_description.js
 * 
 * Code used to display/hide the game description overlay
 */

/** Cached game description overlay */
var _overlay = null
var _isVisible = false

const _left = 0x01
const _right = 0x02
/* Animation FPS */
const _fps = 60
/* Animation time, in ms */
const _animTime = 500
/* How long each frame takes, in ms */
const _frameTime = 1000 / _fps

/** Cache the overlay (if needed) and center it within the window */
function _PrepareGameDescription() {
    if (_overlay == null) {
        _overlay = document.getElementById('floating-game-detail')
    }

    var windowHeight = window.innerHeight
    var yPosition = window.pageYOffset || document.documentElement.scrollTop

    if (_overlay.clientHeight < window.innerHeight) {
        var pos = windowHeight - _overlay.clientHeight
        pos /= 2
        pos += yPosition

        _overlay.style.top = pos+'px'
        _overlay.style.height = ''
        _overlay.style.overflow = 'visible'
    }
    else {
        _overlay.style.top = yPosition+'px'
        _overlay.style.height = windowHeight+'px'
        _overlay.style.overflow = 'auto'
    }
}

/** Globaly stored parameters, to avoid problems with browsers that can't pass
 * parameters to setTimeout */
var _params = {
        dir: _left,
        src: 0,
        dst: 1,
        curTime: 0,
        animTime: 1000,
        frameTime: 16,
        curAnim: -1}

/** Play the animation described in '_params' until its completion */
function _PlayAnimation() {
    _params.curTime += _params.frameTime
    var perc = _params.curTime / _params.animTime
    var pos = _params.src * (1 - perc) + _params.dst * perc
    _overlay.style.left = pos+'px'

    if (_params.curTime < _params.animTime) {
        setTimeout(function() {_PlayAnimation()}, _params.frameTime)
    }
    else {
        /* Ensure there was no rounding errors */
        _overlay.style.left = _params.dst+'px'

        /* If it was hidden, make sure it's not visible anymore */
        if (_params.dir == _left) {
            _overlay.style.visibility = 'hidden'
        }
    }
}

/**
 * Setup '_params' and start the BG job for the animation
 *
 * @param  [ in]dir  Either _left or _right (direction of the movement)
 * @param  [ in]dest Position of the overlay after the animation
 */
function _StartAnimation(dir, dest) {
    _PrepareGameDescription()

    /* Initialize the animation's parameters */
    if (dir == _right) {
        _params.src = -_overlay.clientWidth - 32
    }
    else if (dir == _left) {
        _params.src = 0
    }
    _params.dst = dest
    _params.dir = dir
    _params.animTime = _animTime
    _params.frameTime = _frameTime
    _params.curAnim = -1

    /* Ensure the overlay is on the correct position, and visible */
    if (_params.curTime == 0 || _params.curTime > _params.animTime) {
        _overlay.style.left = _params.src+'px'

        _params.curTime = 0
    }
    else {
        /* Nicely blocks an animation mid-way... Kinda hacky, though... */
        _params.curTime = _animTime - _params.curTime
    }
    _overlay.style.visibility = 'visible'

    /* Start to play it until completition */
    _PlayAnimation()
}

/**
 * Set the title of an event (within the overlay)
 *
 * @param  [ in]ctx   The title element
 * @param  [ in]event The event object
 */
function _SetEventTitle(ctx, event) {
    switch (event.title) {
        case 'Ludum Dare': {
            ctx.innerHTML = 'Ludum Dare Entry Details'
        } break;
    }
}

function _CreateListItem(title, content) {
    var ret = '<li>'
    if (title) {
        ret += ' <strong>' + title + ':</strong>'
    }
    ret += content
    ret += '</li>\n'
    return ret
}

/**
 * Set the content of an event (within the overlay)
 *
 * @param  [ in]ctx   The content element
 * @param  [ in]event The event object
 */
function _SetEventContent(ctx, event) {
    switch (event.title) {
        case 'Ludum Dare': {
            var list = '<ul>\n'
            list += _CreateListItem('Made for', event.title + ' ' + event.edition)
            list += _CreateListItem('Theme', event.theme)
            list += _CreateListItem('', '<a href="' + event.page + '">Entry page</a>')
            list += _CreateListItem('', '<a href="' + event.source + '">Source code</a>')
            list += _CreateListItem('', '<a href="' + event.timelapse + '">Timelapse</a>')
            list += '</ul>\n'
            ctx.innerHTML = list
        } break;
    }
}

/**
 * Fill the overlay with the desired game data
 *
 * @param  [ in]ctx The object that called this function
 */
function SetGameDescription(ctx) {
    _PrepareGameDescription()

    var name = ctx.getAttribute('id')
    var jsonText = document.getElementById(name+'-json').innerText
    if (!jsonText) {
        /* TODO Print error */
        return
    }
    var dataObj = JSON.parse(jsonText)
    if (!dataObj) {
        /* TODO Print error */
        return
    }

    var i
    for (i = 0; i < _overlay.childNodes.length; i++) {
        var child = _overlay.childNodes[i]
        if (child.getAttribute == null) {
            continue
        }

        switch (child.id) {
            case 'detail-title': {
                if (!dataObj.title) {
                    /* TODO Print error */
                    continue
                }
                child.innerHTML = dataObj.title
            } break;
            case 'detail-jam-title': {
                if (!dataObj.event) {
                    child.style.visibility = 'hidden'
                    child.innerHTML = ''
                    continue
                }

                child.style.visibility = 'visible'
                _SetEventTitle(child, dataObj.event)
            } break;
            case 'detail-jam-content': {
                if (!dataObj.event) {
                    child.style.visibility = 'hidden'
                    child.innerHTML = ''
                    continue
                }

                child.style.visibility = 'visible'
                _SetEventContent(child, dataObj.event)
            } break;
            case 'detail-about-title': {
                /* Does nothing */
            } break;
            case 'detail-about': {
                var desc = ''
                var j
                for (j = 0; j < dataObj.description.length; j++) {
                    desc += '<p>'
                    desc += dataObj.description[j]
                    desc += '</p>'
                }
                child.innerHTML = desc
            } break;
            case 'detail-download-title': {
                if (!dataObj.distribution || dataObj.distribution.length == 0) {
                    child.style.visibility = 'hidden'
                    child.innerHTML = ''
                    continue
                }

                if (dataObj.distribution.length > 1) {
                    child.innerHTML = 'Downloads'
                }
                else if (dataObj.distribution[0].mode == 'web') {
                    child.innerHTML = 'Web Game'
                }
                else {
                    child.innerHTML = 'Download'
                }
                child.style.visibility = 'visible'
            } break;
            case 'detail-download': {
                if (!dataObj.distribution || dataObj.distribution.length == 0) {
                    child.style.visibility = 'hidden'
                    child.innerHTML = ''
                    continue
                }

                var j
                var list = '<ul>\n'
                for (j = 0; j < dataObj.distribution.length; j++) {
                    obj = dataObj.distribution[j]

                    if (obj.mode == 'web') {
                        list += _CreateListItem('', '<a href="' + obj.link + '">Play directly in your browser</a>')
                    }
                    else {
                        list += _CreateListItem('', '<a href="' + obj.link + '">Download for <strong>' + obj.mode + '</strong></a>')
                    }
                }
                list += '</ul>\n'
                child.innerHTML = list
                child.style.visibility = 'visible'
            } break;
        }
    }
}

function ShowGameDescription() {
    _PrepareGameDescription()

    _StartAnimation(_right, 0)
    _isVisible = true
}

function HideGameDescription() {
    _PrepareGameDescription()

    _StartAnimation(_left, -_overlay.clientWidth - 32)
    _isVisible = false
}

function ToggleGameDescriptionVisibility() {
    _PrepareGameDescription()

    if (_isVisible) {
        HideGameDescription()
    }
    else if (!_isVisible) {
        ShowGameDescription()
    }
}

/* Setup a event for scrolling, so the overlay is always centered */
var _defaultScroll = document.onscroll
document.onscroll = function() {
    /* Center the overlay whenever the screen scrolls */
    if (_isVisible) {
        _PrepareGameDescription()
    }

    /* Call any previous event handler */
    if (_defaultScroll) {
        _defaultScroll()
    }
}


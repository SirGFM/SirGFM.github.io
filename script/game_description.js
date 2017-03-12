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

    if (_overlay.clientHeight < window.innerHeight) {
        pos = window.innerHeight - _overlay.clientHeight
        pos /= 2
        pos += window.pageYOffset || document.documentElement.scrollTop

        _overlay.style.top = pos+'px'
    }
    else {
        /* TODO Do something if it's bigger than the screen? */
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

function _PlayAnimation() {
    _params.curTime += _params.frameTime
    perc = _params.curTime / _params.animTime
    pos = _params.src * (1 - perc) + _params.dst * perc
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

function _StartAnimation(dir, dest) {
    _PrepareGameDescription()

    /* Initialize the animation's parameters */
    if (dir == _right) {
        _params.src = -_overlay.clientWidth - 32
        _params.dst = 0
    }
    else if (dir == _left) {
        _params.src = 0
        _params.dst = -_overlay.clientWidth - 32
    }
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

function SetGameDescription() {
    _PrepareGameDescription()
}

function ShowGameDescription() {
    _PrepareGameDescription()

    _StartAnimation(_right, 0)
    _isVisible = true
}

function HideGameDescription() {
    _PrepareGameDescription()

    _StartAnimation(_left, -_overlay.clientWidth)
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

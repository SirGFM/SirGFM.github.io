/**
 * 
 */

function ShowGameDetails(ctx) {
    name = ctx.getAttribute('id')
    for (i = 0; i < ctx.childNodes.length; i++) {
        child = ctx.childNodes[i]
        if (child.getAttribute == null) {
            continue
        }
        if (child.getAttribute('class').indexOf('gameiconoverlay') != -1) {
            child.style.visibility = 'visible'
        }
    }
}

function HideGameDetails(ctx) {
    name = ctx.getAttribute('id')
    for (i = 0; i < ctx.childNodes.length; i++) {
        child = ctx.childNodes[i]
        if (child.getAttribute == null) {
            continue
        }
        if (child.getAttribute('class').indexOf('gameiconoverlay') != -1) {
            child.style.visibility = 'hidden'
        }
    }
}

var visible_desc = null
function ShowGameDesc(ctx) {
    name = ctx.getAttribute('id')
    desc = document.getElementById(name + '-desc')
    skip = (visible_desc == desc)
    HideAnyGameDesc()
    if (skip || desc == null) {
        return
    }
    desc.setAttribute('class', 'gamedesc-visible')
    visible_desc = desc
}

function HideAnyGameDesc() {
    if (visible_desc != null) {
        visible_desc.setAttribute('class', 'gamedesc-hidden')
    }
    visible_desc = null
}


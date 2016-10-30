/**
 * 
 */

function ShowGameDetails(ctx, name) {
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

function HideGameDetails(ctx, name) {
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


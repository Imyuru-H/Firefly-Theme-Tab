/**
 * 当有文件拖入的时候，浏览器默认会打开拖入的文件，导致用户跳出我们的应用，为了防止
 * 这个问题的产生，可以对目标元素做一些特殊处理。这样当文件拖到这个目标元素上的时候，
 * 浏览器就不会打开文件了。
 * Tip:可以传入 document 对象，这样无论文件拖到页面任何位置，浏览器都不会打开文件了。
 * @param target {HTMLDocument|HTMLElement|jQuery} 目标
 * @param [onDrop] {Function}
 */

function PreventDefaultFileDrop (target, onDrop) {
    var targetEl;
    // ie9及以下，不支持拖放，所以直接返回false
    if(navigator.appName == "Microsoft Internet Explorer" && parseInt(navigator.appVersion.split(";")[1].replace(/[ ]/g, "").replace("MSIE","")) <= 9){
        return false;
    }
    if (target instanceof jQuery) {
        targetEl = target[0];
    } else if (target instanceof Element || target instanceof Document) {
        targetEl = target;
    } else {
        console.error('Target must be a HTMLDocument|HTMLElement|jQuery.');
    }

    targetEl.ondragover = function () {
        return false;
    };
    targetEl.ondrop = function (e) {
        e.preventDefault();
        onDrop && onDrop();
    };

    document.addEventListener("dragenter", function( event ) {
        undefined;
    }, false);
    document.addEventListener("dragover", function( event ) {
        undefined;
    }, false);
    document.addEventListener("drop", function( event ) {
        event.preventDefault();//禁止浏览器默认行为
        undefined;
        return false;//禁止浏览器默认行为
    }, false);
    document.addEventListener("dragend", function( event ) {
        undefined;
    }, false);
}

window.onload = function(){
    PreventDefaultFileDrop(document);
}
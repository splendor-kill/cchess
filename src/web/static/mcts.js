"use strict";

var LIMIT_DEPTH = 1;

function MCTS(pos, hashLevel) {
    this.hashMask = (1 << hashLevel) - 1;
    this.pos = pos;
    console.log(pos.toFen())
}

MCTS.prototype.searchMain = function (depth, millis) {
    console.log("searchMain here")

    var http = new XMLHttpRequest();
    var url = 'http://127.0.0.1:5000/play';

    console.log(this.pos.toFen())
    http.open('POST', url, true);

    http.setRequestHeader('Content-Type', 'application/json');


    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200) {
            console.log(http.responseText);
        }
    }
    http.send(JSON.stringify({
        'position': this.pos.toFen()
    }));
}
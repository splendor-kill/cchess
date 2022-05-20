"use strict";

var LIMIT_DEPTH = 1;

function MCTS(pos, hashLevel) {
    this.hashMask = (1 << hashLevel) - 1;
    this.pos = pos;
    console.log(pos.toFen())
}

MCTS.prototype.searchMain = function (depth, millis) {
    console.log(this.pos.toFen())

    var http = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/play";
    http.open("POST", url, true);
    http.setRequestHeader("Content-Type", "application/json");

    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200) {
            console.log(http.responseText);
            var s = JSON.parse(http.responseText)["move"]
            var t = [s.slice(0, 2), "-", s.slice(2)].join("").toUpperCase()
            var ret = iccs2Move(t);
            console.log(ret);
            return ret;
        }
    }
    http.send(JSON.stringify({
        "position": this.pos.toFen()
    }));
}

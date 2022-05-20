"use strict";

function CHR(n) {
  return String.fromCharCode(n);
}

function ASC(c) {
  return c.charCodeAt(0);
}

function move2Iccs(mv) {
  var sqSrc = SRC(mv);
  var sqDst = DST(mv);
  return CHR(ASC("A") + FILE_X(sqSrc) - FILE_LEFT) +
      CHR(ASC("9") - RANK_Y(sqSrc) + RANK_TOP) + "-" +
      CHR(ASC("A") + FILE_X(sqDst) - FILE_LEFT) +
      CHR(ASC("9") - RANK_Y(sqDst) + RANK_TOP);
}

function iccs2Move(iccs) {
  var f1 = ASC(iccs[0]) - ASC("A") + FILE_LEFT;
  var r1 = ASC("9") - ASC(iccs[1]) + RANK_TOP;
  var src = COORD_XY(f1, r1);
  var f2 = ASC(iccs[3]) - ASC("A") + FILE_LEFT;
  var r2 = ASC("9") - ASC(iccs[4]) + RANK_TOP;
  var dst = COORD_XY(f2, r2);
  return MOVE(src, dst);
}

function resize() {
  var width = $(window).width();
  var col;
  if (width < 576) {
    col = 1;
  } else if (width < 768) {
    col = 2;
  } else if (width < 992) {
    col = 3;
  } else {
    col = 4;
  }
  var i, j;
  var e = $(".photo-container");
  var container_width = width / col;
  var left = 0, top;
  var last;
  var max_top = 0;
  for (i = 0;i < col;i++) {
    top = 0;
    $(e[i]).css("width", container_width+"px");
    $(e[i]).css("top", top+"px");
    $(e[i]).css("left", left+"px");
    last = i;
    j = i + col;
    while (e[j] !== undefined) {
      top += $(e[last]).height();

      $(e[j]).css("width", container_width+"px");
      $(e[j]).css("top", top+"px");
      $(e[j]).css("left", left+"px");
      last = j;
      j += col;
    }
    top += $(e[last]).height();
    left += container_width;
    if (top > max_top)
      max_top = top;
  }
  $(".album-container").css("height", max_top+"px");
}

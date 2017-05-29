/**
 * Created by chnigkiuchan on 13/1/2017.
 */
function resize() {
  $(".large-container").css("height", $(".wrapper").outerHeight());
}
var main = (function() {
    var x, y;
    var startBackground = function(index) {
          if (index > 4) {
            index = 1
          }
          var top = $("#top");
          top.addClass("background" + index);
          /*
          x = -Math.floor(Math.random() * 100);
          y = -Math.floor(Math.random() * 100);
          top.animate({
              "background-position-x": x + "px",
              "background-position-y": y + "px"
            }, 5000, function() {*/
            setTimeout(function() {
              top.removeClass("background" + index)
              startBackground(index+1);
            }, 5000);
    };

    var jefade = function() {
      var f = $(".jefade");
      var hide_class;
      var show_classes = {
        "show-x": "jefade-show-x",
        "show-y": "jefade-show-y"
      }, show_class;
      var checkOffset = function(e) {
        var top = e.offset().top;
        var bottomY = $(window).scrollTop() + $(window).height();
        if (bottomY > top && !e.hasClass(show_class)) {
          var type = e.attr("data-jefade-type");
          var delay = e.attr("data-jefade-delay") ? e.attr("data-jefade-delay") : 0;
          if (type){
            if (show_classes[type])
              show_class = show_classes[type];
          }
          else {
            show_class = "jefade-show-y";
          }
          setTimeout(function() {e.addClass(show_class);}, delay);
        }
      };
      var onScroll = function() {
        f.each(function(index) {
          checkOffset($(this));
        })
      };
      $(window).bind("scroll", onScroll);
      $(onScroll);
    }

    var currentColor = null;

    return {
        onload: function() {
            var f = new jefade();
            var colorLightness;
            $(".scroll_page").bind('click', function(e) {
              e.preventDefault();
              var href = $(this).attr('href');
              var body = $("html, body");
              var navHeight = $(".navbar").outerHeight();
              body.stop().animate({scrollTop:$(href).offset().top-navHeight+25}, '500', 'swing')
            });

            var onscroll = function() {
              var navHeight = $(".navbar").outerHeight();
              var logoHeight = $("#logo").height();
              var defaultOpacity = 0, opacity, navLogoOp;
              var defaultPosition = 50, position;
              var defaultLogoSize = 120, logoSize;
              var defaultLightness = 100, lightness;
              var delta = $('#logo').offset().top - $(window).scrollTop();
              var offset = navHeight-delta;
              var logOffset = offset/logoHeight
             if (logOffset <= 1 && logOffset >= 0) {
                 var po =  (1 - logOffset) * defaultPosition;
                 position = po < 5 ? 5 : po;
                 lightness = logOffset * defaultLightness;
                 opacity = logOffset + defaultOpacity;
                 logoSize = (1-logOffset) * defaultLogoSize;
             } else if (logOffset > 1) {
                  position = 5;
                  lightness = defaultLightness;
                  opacity = 1;
                  logoSize = 0;
                  colorLightness = 0;
                  $(".globe-button > span").addClass('globe-active')
             } else if (logOffset < 0) {
                  position = defaultPosition;
                  lightness = 0;
                  opacity = defaultOpacity;
                  logoSize = defaultLogoSize;
                  colorLightness = 100;
                  $(".globe-button > span").removeClass('globe-active')
             }
             if (logoSize < 20) {
                  navLogoOp = 1;
             } else {
                  navLogoOp = 0;
             }
             $(".navbar-logo").css('opacity', navLogoOp);
             $(".navbar").css('background-color', 'hsla(0,0%,'+lightness+'%,'+ opacity +')');
             $("ul.navbar-nav li a").css('color', 'hsla(0,0%,'+colorLightness+'%, 1)');
             $(".navbar-header button span.icon-bar").css('background-color', 'hsla(0,0%,'+colorLightness+'%, 1)');

             // header-part end

             // red-apple start
            }
            var heroscroll = function() {

            }
            $(window).bind('scroll', onscroll);
            startBackground(1);

            var flip_cube = function(ele) {
              ele.toggleClass("cube-activate");
            }
            var run = function() {
              $(".cube .faces-container").each(function() {
                if ($(this).hasClass("cube-activate"))
                  flip_cube($(this));
                else {
                  if (Math.random() > Math.random()) {
                    flip_cube($(this));
                  }
                }
              });
              setTimeout(run, 7000);
            }
            $(function() {
              onresize();
              run();
            });

            var images = ["../static/apple/images/1.jpg", "../static/apple/images/2.jpg", "../static/apple/images/3.jpg", "../static/apple/images/4.jpg"
            ,"../static/apple/images/tinyuen/1.jpg","../static/apple/images/tinyuen/2.jpg","../static/apple/images/tinyuen/3.jpg","../static/apple/images/tinyuen/4.jpg"
            ];
            //$("body").css("overflow-y", "hidden");
            var loadImage = function(i) {
              if (images[i] === undefined) {
                $("body").css("overflow-y", "scroll");
                $("div.cover").fadeOut();
              } else {
                var image_src = images[i];
                var image = new Image();
                image.onload = function() {
                  loadImage(i+1);
                };
                image.onerror = function() {
                  alert("error loading " + image_src);
                }
                image.src = image_src;
              }
            };
            //loadImage(0);
            var right = function() {
              $("html, body, #top, .head-content").addClass("whole-right");
              $("#top .head-content .container-fluid .row").addClass("row-right");
              $("#top").removeClass("top-wrong");
              $(".head-content").removeClass("head-content-wrong");
              $("html, body, #top, .head-content").removeClass("whole-wrong");
            }
            var wrong = function() {
              $(".head-content").addClass("head-content-wrong");
              $("#top").addClass("top-wrong");
              $("html, body, #top, .head-content").addClass("whole-wrong");
              $("html, body, #top, .head-content").removeClass("whole-right");
              $("#top .head-content .container-fluid .row").removeClass("row-right");
            }
            var onresize = function() {
              var width = $(window).width();
              var height = $(window).height();
              var aspect_ratio = width / height;
              if (aspect_ratio >= 1.25 && aspect_ratio <= 1.9) {
                if (width > 768) {
                  right();
                }else
                  wrong();
              } else {
                wrong();
              }
            };
            $(window).on("resize", onresize);
        }
    };
})();

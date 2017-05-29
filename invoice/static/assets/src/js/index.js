global.jQuery = require('jquery')
var $ = require("jquery")
import {TweenMax, Power2, TimelineLite} from "gsap";
require('bootstrap');


function resize() {
//  $("#main-container").css("max-width", $(window).height() / 3 * 3 + "px");
}
$(function() {
  resize();
  $(window).resize(resize)
  var delay = 0;
  var startAnimation = new TimelineMax();
  var grid = $(".grid");
  var duration = 0.5, delay = 0, stagger = "-=0.25";
  var active = false;

  startAnimation.from(grid[0], duration, {x: "100%",y: "100%",ease: Bounce.easeOut,delay: 1}, stagger)
    .from(grid[1], duration, {y: "100%",ease: Bounce.easeOut,delay: delay}, stagger)
    .from(grid[2], duration, {x: "-100%",y: "100%",ease: Bounce.easeOut,delay: delay}, stagger)
    .from(grid[3], duration, {x: "100%",ease: Bounce.easeOut,delay: delay}, stagger)
    .from(grid[6], duration, {x:"-100%", y: "-100%",ease: Bounce.easeOut,delay: delay}, stagger)
    .from(grid[7], duration, {x:"100%", y: "-200%",ease: Bounce.easeOut,delay: delay}, stagger)
    .from(grid[8], duration, {y: "-200%",ease: Bounce.easeOut,delay: delay}, stagger)
    .from(grid[5], duration, {y: "-100%",ease: Bounce.easeOut,delay: delay}, stagger)
    .from(grid[9], duration, {x:"-100%", y: "-200%",ease: Bounce.easeOut,delay: delay, onComplete: function() {
      $(".window, .apple-svg").addClass("apple_animated");
    }}, stagger);

  var collect = [], expand = [], showDetail = new TimelineMax();
  var complete = function() {

  };
  for (var i = 0;i < 3;i++) {
    collect[i] = new TimelineMax({onComplete: function() {
      active = false;
    }});
    expand[i] = new TimelineMax({onComplete: function() {
      active = false;
    }});
  }

  var expand_onComplete = function(index) {
    $(grid[index]).toggleClass("active");
    switch (index) {
      case 0: {

        break;
      }
      case 1: {
        break;
      }
      case 2: {
        break;
      }
    }
  }

  collect[0].to(grid[0], duration, {scale: 1.3, ease:Elastic.easeOut})
    .to(grid[1], duration, {x: "-100%",delay: delay}, stagger)
    .to(grid[2], duration, {x: "-200%",delay: delay}, stagger)
    .to(grid[3], duration, {autoAlpha: 0,delay: delay}, 0)
    .to(grid[4], duration, {autoAlpha: 0,delay: delay}, 0)
    .to(grid[5], duration, {x: "-100%", y: "-200%",delay: delay}, stagger)
    .to(grid[6], duration, {x:"-200%", y: "-200%",delay: delay}, stagger)
    .to(grid[0], duration, {x:"100%",y:"100%", scale: 3,ease:Elastic.easeOut}, stagger)
    .to($(grid[0]).children().children("#card"), duration+0.2, {
      rotationY: 180, ease:Elastic.easeOut, onComplete:function() {
        $("#apple-content").fadeIn();
      }
    }, stagger).pause()

  expand[0].to($(grid[0]).children().children("#card"), duration, {rotationY: 0})
    .to(grid[0], duration, {x:"0%",y:"0%", scale: 1, ease:Elastic.easeOut}, stagger)
    .to(grid[6], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[5], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[4], duration, {autoAlpha: 1,delay: delay}, "-=" + duration)
    .to(grid[3], duration, {autoAlpha: 1,delay: delay}, "-=" + duration)
    .to(grid[2], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[1], duration, {x: "0%",y: "0%",delay: delay, onComplete: function() {expand_onComplete(0)}}, stagger)
  .pause()

  collect[1].to(grid[1], duration, {scale: 1.3, ease:Elastic.easeOut})
    .to(grid[0], duration, {x: "100%",delay: delay}, stagger)
    .to(grid[2], duration, {x: "-100%",delay: delay}, stagger)
    .to(grid[3], duration, {autoAlpha: 0,delay: delay}, "-=" + duration)
    .to(grid[4], duration, {autoAlpha: 0,delay: delay}, "-=" + duration)
    .to(grid[5], duration, {y: "-200%",delay: delay}, stagger)
    .to(grid[6], duration, {x:"-100%", y: "-200%",delay: delay}, stagger)
    .to(grid[1], duration, {y:"100%", scale: 3, ease:Elastic.easeOut}, stagger)
    .to($(grid[1]).children().children("#card"), duration+0.2, {
      rotationY: 180, ease:Elastic.easeOut, onComplete:function() {
        $("#wooden-content").fadeIn();
      }
    }, stagger)
    .pause();

  expand[1].to($(grid[1]).children().children("#card"), duration, {rotationY: 0})
    .to(grid[1], duration, {x:"0%",y:"0%", scale: 1, ease:Elastic.easeOut}, stagger)
    .to(grid[6], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[5], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[4], duration, {autoAlpha: 1,delay: delay}, "-=" + duration)
    .to(grid[3], duration, {autoAlpha: 1,delay: delay}, "-=" + duration)
    .to(grid[2], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[0], duration, {x: "0%",y: "0%",delay: delay, onComplete: function() {expand_onComplete(1)}}, stagger)
  .pause()

  collect[2].to(grid[2], duration, {scale: 1.3, ease:Elastic.easeOut})
    .to(grid[0], duration, {x: "200%",delay: delay}, stagger)
    .to(grid[1], duration, {x: "100%",delay: delay}, stagger)
    .to(grid[3], duration, {autoAlpha: 0,delay: delay}, "-=" + duration)
    .to(grid[4], duration, {autoAlpha: 0,delay: delay}, "-=" + duration)
    .to(grid[5], duration, {x: "100%", y: "-200%",delay: delay}, stagger)
    .to(grid[6], duration, {y: "-200%",delay: delay}, stagger)
    .to(grid[2], duration, {x:"-100%",y:"100%", scale: 3, ease:Elastic.easeOut}, stagger)
    .to($(grid[2]).children().children("#card"), duration+0.2, {
      rotationY: 180, ease:Elastic.easeOut, onComplete:function() {
        $("#new-content").fadeIn();
      }
    }, stagger)
    .pause();

  expand[2].to($(grid[2]).children().children("#card"), duration, {rotationY: 0})
    .to(grid[2], duration, {x:"0%",y:"0%", scale: 1, ease:Elastic.easeOut}, stagger)
    .to(grid[6], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[5], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[4], duration, {autoAlpha: 1,delay: delay}, "-=" + duration)
    .to(grid[3], duration, {autoAlpha: 1,delay: delay}, "-=" + duration)
    .to(grid[1], duration, {x: "0%",y: "0%",delay: delay}, stagger)
    .to(grid[0], duration, {x: "0%",y: "0%",delay: delay, onComplete: function() {expand_onComplete(2)}}, stagger)
  .pause()

  $("#apple").click(function() {
    if (!active) {
      $(this).toggleClass("active");
      collect[0].restart();
      active = true;
    }
  });
  $("#apple-content .close-button").click(function() {
    if (!active) {
      active = true;
      $("#apple-content").fadeOut(function() {
        expand[0].restart();
      });
    }
  });

  $("#wooden_white").click(function() {
    if (!active) {
      $(this).toggleClass("active");
      collect[1].restart();
      active = true;
    }
  });
  $("#wooden-content .close-button").click(function() {
    if (!active) {
      active = true;
      $("#wooden-content").fadeOut(function() {
        expand[1].restart();
      });
    }
  });

  $("#new").click(function() {
    if (!active) {
      active = true;
      $(this).toggleClass("active");
      collect[2].restart();
    }
  });
  $("#new-content .close-button").click(function() {
    if (!active) {
      active = true;
      $("#new-content").fadeOut(function() {
        expand[2].restart();
      });
    }
  });
});

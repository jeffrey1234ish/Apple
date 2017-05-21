/**
 * Created by JeffreyChan on 11/11/2016.
 */
 var ProductInfo = function(id, name, serial, price, colors, iw) {
    this.id = id;
    this.name = name;
    this.serial_number = serial;
    this.price = price;
    this.colors = colors;
    this.is_wardrobe = iw;
}
var ProductColors = {
    walnut: {
        'chinese': "淺胡桃",
        'letter': 'L'
    },
    black: {
        'chinese': '黑橡木',
        'letter': 'B'
    },
    cherry: {
      'chinese': '紅櫻桃',
      'letter': 'R'
    },
    white: {
        'chinese': '白木紋',
        'letter': 'W'
    },
    maple: {
        'chinese': '楓木',
        'letter': 'M'
    },
    oak: {
        'chinese': '橡木',
        'letter': 'A'
    },
    glossy_white: {
        'chinese': '白亮光',
        'letter': 'G'
    },
    black_white: {
        'chinese': '黑橡/白',
        'letter': 'BW'
    },
    cherry_white: {
        'chinese': '紅櫻桃/白',
        'letter': 'CW'
    },
    walnut_white: {
        'chinese': '淺胡桃/白',
        'letter': 'WW'
    },
    glossy_champagne: {
        'chinese': '香檳亮光',
        'letter': 'GC'
    },
    wooden_champagne: {
        'chinese': '香檳木紋',
        'letter': 'C'
    },
    other: {
        'chinese': '其他',
        'letter': 'O'
    }
}
var letter_to_english = function(letter) {
    for (var color in ProductColors) {
      if (ProductColors[color].letter === letter)
        return color;
    }
}
var letter_to_chinese = function(letter) {
    for (var color in ProductColors) {
      if (ProductColors[color].letter === letter)
        return ProductColors[color].chinese;
    }
}
var d = function (id) {
    return document.getElementById(id);
}

// data provided by wikipedia:
var HKRegions = {
  "香港島":["金鐘", "上環", "中環", "銅鑼灣", "灣仔", "大坑", "太古", "柴灣", "西環", "天后", "北角", "跑馬地", "杏花邨"],
  "九龍":["油麻地", "深水埗", "九龍城", "黃大仙", "觀塘", "旺角", "尖沙咀", "太子", "何文田", "佐敦", "美孚", "九龍塘", "九龍灣", "土瓜灣", "樂富"],
  "新界": ["葵涌", "葵芳", "荃灣", "深井", "天水圍", "粉嶺", "火炭", "青衣", "將軍澳", "屯門", "元朗", "北區", "大埔", "大圍", "沙田", "西貢"],
  "離島": ["大嶼山", "南丫島", "愉景灣", "大澳", "東涌", "長洲"]
};

var tagsToReplace = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
};

function replaceTag(tag) {
    return tagsToReplace[tag] || tag;
}

function safe_tags_replace(str) {
    return str.replace(/[&<>]/g, replaceTag);
}

var apple = (function() {
  var staredObjects = function() {
      return typeof(localStorage.stared) === "undefined" ? [] : JSON.parse(localStorage.stared);
  };
  var isInvoiceInStared = function(id) {
    var stared = staredObjects();
    var i = 0, flag = false;
    while (i < stared.length && flag == false) {
        if (stared[i].id == id)
            flag = true;
        i++;
    }
    return flag;
  };

  var staredInvoiceIndex = function(id) {
      var stared = staredObjects();
      var i = 0;
        while (i < stared.length) {
            if (stared[i].id == id)
                return i;
            i++;
        }
        return -1;
  };

  var addInvoiceItem = function(object) {
      var stared = staredObjects();
      stared.push(object);
      localStorage.stared = JSON.stringify(stared);
  };

  var removeInvoiceWithId = function(id) {
      var index = staredInvoiceIndex(id);
      if (index != -1) {
          var stared = staredObjects();
          stared.splice(index, 1);
          localStorage.stared = JSON.stringify(stared);
          return true;
      }
      return false;
  }

  var a = {};

  a.onload = function() {
    var iphoneWebAppInplementation = (function() {
      if (window.navigator.standalone) {
        var a = document.getElementsByTagName("a");
        for (var i = 0; i < a.length; i++) {
          if (!a[i].onclick && a[i].getAttribute("target") != "_blank") {
            a[i].onclick = function () {
              window.location = this.getAttribute("href");
              return false;
            }
          }
        }
        /*$("body").css("padding-bottom", "17%");
        $("body").append('<footer id="iphone-navigator" style="z-index: 100;position:fixed;bottom:0;right:0;left:0;height:10%;background:#F3F3F3;border-top: 1px solid #E2E2E2;"></footer>');
        var nav = $("#iphone-navigator");
        var style = '<style>#iphone-navigator a {\nwidth: 20%;height: 100%;margin: 0 5%;background: black;\n} #iphone-navigator a span {font-size: 5vw;}</style>';
        $("head").append(style);
        nav.append("<a href='javascript: void(0)'></a><a href='javascript: void(0)'></a>");*/
      }
    })();

    // This function gets cookie with a given name
    var getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    var csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    var sameOrigin = function(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
  };

  a.root = {};
  a.root.onload = function() {
      var stared = staredObjects();
      var item;
      if (stared.length > 0) {
          for (var i = 0; i < stared.length; i++) {
              item = '<li class="stared_list_item">';
              item += '<a href="/invoice/search/' + stared[i].id + '">';
              item += '<div id="detail_container"><strong><span id="first_name">' + stared[i].name;
              item += '</span></strong><span id="address">' + stared[i].address + '</span><span class="invoice_id">' + stared[i].id + '</span></div></a></li>';

              $("#stared_invoices_list").append(item);
          }
      } else {
          item = '<li class="stared_list_item"><p>沒有重要訂單...</p></li>';
          $("#stared_invoices_list").append(item);
      }
  };
  var showModal = function(txt) {
    $("#alert .modal-body p").html(txt);
    $("#alert").modal('show');
  }
  a.edit = {};
  a.edit.onready = function() {
      var hashchange = function() {
        //.. work ..
        var hash = location.hash;
        switch (hash) {
          case "": {
            $("#search_container").css({"display": "block"});
            qbox.hide();
            custom_qbox.hide();
            break;
          }
          case "#add_product": {
            $("#search_container").css({"display": "none"});
            qbox.show();
            break;
          }
          case "#add_custom_product": {
            $("#search_container").css({"display": "none"});
            custom_qbox.show();
            break;
          }
        }
      };
      var products = [];
      var total_amount = parseInt($("#total_amount").val());
      var deposit = parseInt($("input[name='deposit']").val())
      var discount = parseInt($("#discount").val())
      var setTotalAmount = function(v) {
          total_amount += v;
          d("total_amount").value = total_amount;
      };

      // request to database for invoice products and custom invoice products
      $("#loader").show();
      $.ajax({
        "url": window.location.href+"/invoice_products",
        "method": "GET",
        "error": function (a, b, errorString) {
          console.log("Error: " + errorString)
        }
      }).done(function (data) {
        var result = data.result;
        if (result) {
          for (var i = 0;i < result.length;i++) {
            var invoice_product = result[i];
            products.push({
              custom: false,
              id: invoice_product.product.product_id,
              quantity: invoice_product.quantity,
              side_note: invoice_product.side_note,
              color: invoice_product.color,
              price: invoice_product.product.price,
              serial_number: invoice_product.product.serial_number,
              name: invoice_product.product.description
            });
          }
        }
        $.ajax({
          "url": window.location.href+"/invoice_custom_products",
          "method": "GET",
          "error": function (a, b, errorString) {
            console.log("Error: " + errorString)
          }
        }).done(function (data) {
          var result = data.result;
          if (result) {
            for (var i = 0;i < result.length;i++) {
              var product = result[i];
              product.custom = true;
              products.push(product);
            }
          }
          $("#loader").hide();
        });
      });

      var qbox = new QuantityBox(function(p) {
          if (p.quantity <= 0) {
               showModal("請輸入貨品數量")
               return false;
          } else if (p.color === null) {
               showModal("請選擇貨品顏色");
              return false;
          } else if(p.color == "O" && p.side_note == "") {
               showModal("請備註貨品顏色");
               return false;
          } else {
              var s_n = safe_tags_replace(p.side_note);

              var content = '<div class="product_cell"><p id="name_tag"><span id="serial_tag">' + p.serial_number + '</span></p>';
              content += '<p id="color_tag">' + letter_to_chinese(p.color) + '</p><p id="side_note_tag">' + s_n + '</p>';
              content += '<p class="quantity">$<span id="price_tag">' + p.price + '</span> X <span id="quantity_tag">' + p.quantity + '</span></p><a href="javascript: void(0)" class="product_cancel_button"/></a>';
              content += '</div>';

              $("#product_cell_container").append(content);

              total_amount += parseInt(p.price) * parseInt(p.quantity);
              d("total_amount").value = total_amount;

              products.push(p);
          }
          set_cancel_button_onclick();
      });
      var custom_qbox = new CustomQuantityBox(function(p) {
          if (p.quantity <= 0) {
               showModal("請輸入貨品數量");
               return false;
          } else if (p.color == "") {
               showModal("請輸入貨品顏色");
              return false;
          } else if(p.price <= 0) {
               showModal("請輸入貨品銀碼");
               return false;
          } else if(p.name == "") {
               showModal("請輸入貨品名稱");
               return false;
          } else {
              var s_n = safe_tags_replace(p.side_note);
              var c = safe_tags_replace(p.color);
              var n = safe_tags_replace(p.name);

              var content = '<div class="product_cell"><p id="name_tag"><span id="serial_tag">' + n + '</span></p>';
              content += '<p id="color_tag">' + c + '</p><p id="side_note_tag">' + s_n + '</p>';
              content += '<p class="quantity">$<span id="price_tag">' + p.price + '</span> X <span id="quantity_tag">' + p.quantity + '</span></p><a href="javascript: void(0)" class="product_cancel_button"/></a>';
              content += '</div>';
              $("#product_cell_container").append(content);

              setTotalAmount(parseInt(p.price) * parseInt(p.quantity));

              products.push(p);
          }
          set_cancel_button_onclick();
      });

      var search_button_clicked = function() {
          // when the search button is pressed
          $("#loader").show();
          qbox.getProducts(d("search_string_text_box").value, function(info){
              if (info.length > 0) {
                  d("edit_product_container").innerHTML = "";
                  var p;
                  for(var i=0,len=info.length;i < len;i++) {
                        p = info[i];
                        var content = '<a class="product-choice" href="javascript: void(0)"id="product_' + i + '">  '
                        content += '<div class="product_content_container">'
                        content += '<p class="product_info_tag">' + p.serial_number + '</p><p>' + p.name +'</p> <p class="product_info_tag">價錢: $' + p.price + '</p></div> '
                        content += ' </a>'
                        $("#edit_product_container").append(content);
                        $("#product_" + i).click(function() {
                            qbox.next(info[this.id.split("_")[1]]);
                        });
                  }
              } else {
                d("edit_product_container").innerHTML = "<p>找不到傢俬..</p>";
              }
              $("#loader").hide();
          });
      };

      var set_cancel_button_onclick = function() {
          $("body").css("overflow-y", "scroll");
          $(".product_cancel_button").click(function() {
              $(this).parent().animate({
                  'opacity': 0,
                  'padding': 0
              }, 400, function() {
                  var index = $(this).index();
                  var deleted_product = products.splice(index, 1)[0];
                  total_amount -= (deleted_product.quantity * deleted_product.price);
                  d("total_amount").value = total_amount;
                  $(this).remove();
              });
          });
      };
      $("#submit_search_button").on("click", search_button_clicked);

      // on form submit
      // create and return product in an array format
      $("#form").submit(function(e) {
          deposit = parseInt($("input[name='deposit']").val())
          discount = parseInt($("#discount").val())
          total_amount = parseInt(d('total_amount').value);
          if (total_amount-deposit-discount < 0) {
              if (!confirm("確定訂金 $"+deposit+"?")) {
                  return false;
              }
          }
          for (var i=0,len=products.length;i<len;i++) {
              var input_name = "product_" + i;

              var object;
              if (products[i].custom == true) {
                  object = {
                    'custom': products[i].custom,
                    'name': encodeURI(products[i].name),
                    'quantity': products[i].quantity,
                    'price': products[i].price,
                    'color': encodeURI(products[i].color),
                    'side_note': encodeURI(products[i].side_note)
                  }
              } else {
                  var side_note = products[i].side_note;
                  var id = products[i].id;
                  var quantity = products[i].quantity;
                  object = {
                      'custom': products[i].custom,
                      'color': products[i].color,
                      'id': id,
                      'quantity': quantity,
                      'side_note': encodeURI(side_note)
                  }
              }
              var input = '<input type="hidden" name="' + input_name + '" value=' + JSON.stringify(object) + ' />'
              $(this).append(input);
              console.log(JSON.stringify(object));
          }
      });
      set_cancel_button_onclick();

      hashchange();
      $(window).on('hashchange', hashchange);
  };
  a.edit.custom = {};
  a.edit.custom.onready = function() {
      var hashchange = function() {
        //.. work ..
        var hash = location.hash;
        switch (hash) {
          case "": {
            box.hide();
            $("#search_container").css({"display": "block"});
            break;
          }
          case "#add_product": {
            box.show();
            $("#search_container").css({"display": "hidden"});
            break;
          }
        }
      };
      var products = [];
      $.ajax({
        "url": window.location.href+"/invoice_custom_products",
        "method": "GET",
        "error": function (a, b, errorString) {
          console.log("Error: " + errorString)
        }
      }).done(function (data) {
        var result = data.result;
        if (result) {
          for (var i = 0;i < result.length;i++) {
            var product = result[i];
            products.push({
              custom:true,
              name: product.name,
              id: product.id,
              quantity: product.quantity,
              side_note: product.side_note,
              color: product.color,
              price: product.price,
            });
          }
        }
      });
      var total_amount = parseInt($("#total_amount").val());
      var setTotalAmount = function(v) {
          total_amount += v;
          d("total_amount").value = total_amount;
      }
      var set_cancel_button_onclick = function() {
          $(".product_cancel_button").click(function() {
              $(this).parent().animate({
                  'opacity': 0,
                  'padding': 0
              }, 400, function() {
                  var index = $(this).index();
                  var deleted_product = products.splice(index, 1)[0];
                  setTotalAmount(-(deleted_product.quantity * deleted_product.price));
                  $(this).remove();
              });
          });
      }
      var box = new CustomQuantityBox(function(p) {
          if (p.quantity <= 0) {
               showModal("請輸入貨品數量");
               return false;
          } else if (p.color == "") {
               showModal("請輸入貨品顏色");
              return false;
          } else if(p.price <= 0) {
               showModal("請輸入貨品銀碼");
               return false;
          } else if(p.name == "") {
               showModal("請輸入貨品名稱");
               return false;
          } else {
              var content = '<div class="product_cell"><p id="name_tag"><span id="serial_tag">' + p.name + '</span></p>';
              content += '<p id="color_tag">' + p.color + '</p><p id="side_note_tag">' + p.side_note + '</p>';
              content += '<p class="quantity">$<span id="price_tag">' + p.price + '</span> X <span id="quantity_tag">' + p.quantity + '</span></p><a href="javascript: void(0)" class="product_cancel_button"/></a>';
              content += '</div>';
              $("#product_cell_container").append(content);

              setTotalAmount(parseInt(p.price) * parseInt(p.quantity));

              products.push(p);
          }
          set_cancel_button_onclick();
      })

      $("#form").submit(function(e) {
          var deposit = parseInt($("input[name='deposit']").val())
          var discount = parseInt($("#discount").val())
          total_amount = parseInt(d('total_amount').value);
          if (total_amount-deposit-discount < 0) {
              if (!confirm("確定訂金 $"+deposit+"?")) {
                  return false;
              }
          }
          for (var i=0,len=products.length;i<len;i++) {
              var input_name = "product_" + i;

              var side_note = products[i].side_note;
              var color = products[i].color;
              var name = products[i].name;
              var quantity = products[i].quantity;
              var price = products[i].price
              var object = {
                'custom': products[i].custom,
                'name': encodeURI(name),
                'quantity': quantity,
                'price': price,
                'color': encodeURI(color),
                'side_note': encodeURI(side_note)
              }
              var input = '<input type="hidden" name="' + input_name + '" value=' + JSON.stringify(object) + ' />'
              $(this).append(input);
          }
      });
      set_cancel_button_onclick();

      hashchange();
      $(window).on('hashchange', hashchange);
  }

  a.create = {};
  a.create.onload = function() {
      console.log("hhas");
      for (var region in HKRegions) {
        var group = $('<optgroup label="' + region + '"></optgroup>');
        $("#region_select").append(group);
        for (var i = 0;i < HKRegions[region].length;i++) {
          group.append('<option value="' + HKRegions[region][i] + '">' + HKRegions[region][i] + '</option>');
        }
      }
  };
  a.create.onready = function() {
      $("form").submit(function() {
          var name = $("input[name='first_name']").val();
          var address = $("input[name='address']").val();
          var region = $("#region_select").val();
          var contact = $("input[name='contact_number']").val();

          if (contact==""||address==""||name=="") {
              alert("有項目未填寫!");
              return false;
          } else {
            if (region != null)
              $("input[name='address']").val(region + address);
          }
      })
  };

  a.search = {};
  a.search.onready = function() {
      var invoice_id = $("#invoice_id").html();
      var name = $("#first_name").html();
      var address = $("#address").html();

      if (typeof(Storage) !== "undefined") {
        if (isInvoiceInStared(invoice_id)) {
            $("#star").addClass("stared");
        } else {
            $("#star").addClass("not_stared");
        }
      }

      $("#star").click(function() {
          if (staredInvoiceIndex(invoice_id) != -1) {
              removeInvoiceWithId(invoice_id);
              $(this).removeClass("stared");
              $(this).addClass("not_stared");
          } else {
              addInvoiceItem({'id': invoice_id, 'name': name, 'address': address});
              $(this).addClass("stared");
              $(this).removeClass("not_stared");
          }
      });

      var delete_link = $("#delete_button") ? $("#delete_button").attr("href") : '';
      var complete_link = $("#complete_button") ? $("#complete_button").attr("href") : '';
      var print_link = $("#print_button") ? $("#print_button").attr("href") : '';
      var simpleDraw;
      if (delete_link != '') {
          $("#delete_button").attr("href", "javascript: void(0)");
          $("#delete_button").click(function() {
              if(confirm("你確定要刪除此訂單?")) {
                  window.location.href = delete_link;
              } else {
                  return false;
              }
          });
      }
      if (complete_link != '') {
          $("#complete_button").attr("href", "javascript: void(0)");
          $("#complete_button").click(function() {
              if(confirm("你確定要完成此訂單?")) {
                  window.location.href = complete_link;
              } else {
                  return false;
              }
          });
      }
      if (print_link != '') {
          $("#print_button").attr("href", "javascript: void(0)");
          $("#print_button").click(function() {
              if(confirm("你確定要列印此訂單?")) {
                  window.location.href = print_link;
              } else {
                  return false;
              }
          });
      }
      $("#draw_button").click(function() {
          $(".backdrop").fadeIn();
          if (!simpleDraw) {
              simpleDraw = new DrawingBoard.Board('simple-draw', {
                  controls: false,
                  webStorage: false
              });
          }
      });
      $("#draw_close_button").click(function() {
          var data = simpleDraw.getImg();
          console.log("start sending...");
          $("#backdrop").fadeOut();
          /* $.ajax({
               'type': 'POST',
               'url': "http://" + window.location.href.split('/')[2] + "/invoice/drawing/",
               'data': {'invoice': invoice_id, 'image': data},
                'success': function() {
                   $("#backdrop").fadeOut();
                },
               'error': function(e) {
                   console.log(e);
               }
           });*/
      });
      $("#draw_clear_button").click(function() {
          simpleDraw.resetBackground();
      });
  };

  a.check = {};
  a.check.onready = function() {

  };
  return a;
})();

$(document).ready(apple.onload);

/**
 * Created by JeffreyChan on 24/11/2016.
 */
var d = function (id) {
    return document.getElementById(id);
}
var QuantityBox = function(confirm, cancel, cancel2) {
  var backdrop, quantity_box, search_box;

  var current_product_info;
  var name, serial, price, quantity, side_note, check_box;

  var color_buttons = {};

  var cancel_button, confirm_button, dismiss_button;

  var wardrobe_color_container, color_selection;
  var door_color, door_frame_color, wardrobe_color;

  var setup = function() {
      name = d("name_box_tag");
      serial = d("serial_box_tag");
      price = d("price_box_tag");
      quantity = d("quantity_box_input");
      side_note = d("side-note");

      cancel_button = $("#cancel-button");
      confirm_button = $("#confirm-button");

      for (var color in ProductColors) {
          color_buttons[color] = d(color);
          console.log(color_buttons[color])
      }

      wardrobe_color_container = $("#wardrobe_color_container");
      color_selection = $("#color_selection");
      door_color = $("#door_color");
      door_frame_color = $("#door_frame_color");
      wardrobe_color = $("#wardrobe_color");
  }

  var confirm_button_flag = true;
  backdrop = $("#backdrop");
  quantity_box = $("#quantity_selection_box")
  search_box = $("#product_search_box")
  setup();
  cancel_button.html("上一步");
  cancel_button.click(function() {
    if (typeof cancel == "function") {
        if (cancel() != false) {
            quantity_box.fadeOut(300, function () {
                search_box.fadeIn(300);
            });
        }
    }
    else
        quantity_box.fadeOut(300, function () {
            search_box.fadeIn(300);
        });
  });
  confirm_button.click(function() {
    if (confirm_button_flag) {
      confirm_button_flag = false;
      if (confirm(quantity_box_onconfirm()) != false){
        backdrop.fadeOut(300, function() {
          confirm_button_flag = true;
          window.history.back();
        });
      } else {
        confirm_button_flag = true;
      }
    }
  });
  // activated when confirm button is clicked in quantity_box
  var quantity_box_onconfirm = function () {
    // calculate total price
    var q = quantity.value != '' ? (parseInt(quantity.value) == NaN ? -1 : parseInt(quantity.value)) : 0;
    var s_n = side_note.value;

    if (!current_product_info.is_wardrobe) {
      for (var color in color_buttons) {
          if (color_buttons[color].checked) {
              return {
                custom: false,
                id: current_product_info.id,
                quantity: q,
                side_note: s_n,
                color: ProductColors[color].letter,
                price: current_product_info.price,
                serial_number: current_product_info.serial_number,
                name: current_product_info.name
              };
          }
      }
      return {
        custom: false,
        id: current_product_info.id,
        quantity: q,
        side_note: s_n,
        color: null,
        price: current_product_info.price,
        serial_number: current_product_info.serial_number,
        name: current_product_info.name
      };
    } else {
      w_color = wardrobe_color.val() !== "" ? "櫃身:" + wardrobe_color.val() : "";
      d_f_color = door_frame_color.val() !== "" ? " 門框:" + door_frame_color.val() : "";
      d_color = door_color.val() !== "" ? " 門板:" + door_color.val() : "";
      var wardrobe_note = w_color+ d_f_color + d_color + " | " + s_n;
      return {
        custom: false,
        id: current_product_info.id,
        quantity: q,
        side_note: wardrobe_note,
        color: ProductColors["other"].letter,
        price: current_product_info.price,
        serial_number: current_product_info.serial_number,
        name: current_product_info.name
      };
    }
  }
  var setupQuantitySelectionBox = function(p_info) {
    name.innerHTML = p_info.name;
    serial.innerHTML = p_info.serial_number;
    price.innerHTML = p_info.price;
    quantity.value = '';
    side_note.value = '';

    for (var color in p_info.colors) {
      color_buttons[color].checked = false;
      color_buttons[color].disabled = !p_info.colors[color];
    }
    color_selection.css("display", "block");
    wardrobe_color_container.css("display", "none");
  }
  var setupWardrobeQuantityBox = function(p_info) {
    name.innerHTML = p_info.name;
    serial.innerHTML = p_info.serial_number;
    price.innerHTML = p_info.price;
    quantity.value = '';
    side_note.value = '';

    door_color.val('');
    door_frame_color.val('');
    wardrobe_color.val('');

    color_selection.css("display", "none");
    wardrobe_color_container.css("display", "block");
  }
  this.show = function(duration) {
      search_box.css("display", "block");
      quantity_box.css("display", "none");
      backdrop.fadeIn(duration);
  }
  this.hide = function() {
    search_box.css("display", "block");
    quantity_box.css("display", "none");
    backdrop.fadeOut();
  }
  this.getProducts = function(searchString, done) {
      var products = [];
      if (searchString != '') {
          $.ajax({
            "url": "/invoice/furniture/?searchString=" + searchString,
            "method": "GET",
            "error": function (a, b, errorString) {
              console.log("Error: " + errorString)
            }
          }).done(function (data) {
            var result = data.result;
            if (result) {
                var p;
                for (var i = 0, len = result.length; i < len; i++) {
                    p = result[i];
                    var id = p.product_id;
                    var name = p.description;
                    var serial = p.serial_number;
                    var price = p.price;
                    var colors = {
                        'cherry': p.Red_Cherry, 'walnut': p.Light_Walnut,
                        'black': p.Wooden_Black, 'white': p.Wooden_White, 'maple': p.Maple, 'oak': p.Oak, 'glossy_white': p.Glossy_White,
                        'black_white': p.Black_White, 'cherry_white': p.Cherry_White, 'walnut_white': p.Walnut_White, 'glossy_champagne': p.Glossy_Champagne, 'wooden_champagne': p.Wooden_Champagne,
                        'other': p.Other
                    };
                    var iw = p.is_wardrobe;
                    var info = new ProductInfo(id, name, serial, price, colors, iw);
                    products.push(info);
                }
            }
            console.log(products);
            if (typeof done == "function")
              done(products);
          });
      }
  }
  this.next = function(info) {
    current_product_info = info;
    search_box.fadeOut(300, function() {
      if(info.is_wardrobe) {
        setupWardrobeQuantityBox(info);
      }else {
        setupQuantitySelectionBox(info);
      }
      quantity_box.fadeIn(300);
    });
  }
};

var CustomQuantityBox = function(onconfirm, oncancel) {
    var custom_price = $("#custom_price");
    var custom_color = $("#custom_color");
    var custom_note = $("#custom_side-note");
    var custom_quantity = $("#custom_quantity");
    var custom_name = $("#custom_name");
    var box = $("#custom_backdrop");
    var custom_width = $("#custom_size_1"), custom_depth = $("#custom_size_2"), custom_height = $("#custom_size_3");
    var confirm_button_flag = true;

    this.show = function() {
        custom_price.val('');
        custom_quantity.val('');
        custom_height.val('');
        custom_width.val('');
        custom_depth.val('');
        custom_note.val('');
        custom_name.val('');
        custom_color.val('');
        box.fadeIn();
    };
    this.hide = function() {
      box.fadeOut();
    }
    $("#custom-confirm-button").click(function() {
        var size = (custom_width.val() != 0 && custom_height.val() != 0 && custom_depth.val() != 0)? custom_width.val() + "x" + custom_depth.val() + "x" + custom_height.val() : null
        var product = {
            custom: true,
            name: size !== null ? custom_name.val() + " " + size : custom_name.val(),
            price: custom_price.val() != '' ? (parseInt(custom_price.val()) == NaN ? -1 : parseInt(custom_price.val())) : 0,
            quantity: custom_quantity.val() != '' ? (parseInt(custom_quantity.val()) == NaN ? -1 : parseInt(custom_quantity.val())) : 0,
            side_note: custom_note.val(),
            color: custom_color.val()
        };
        if (confirm_button_flag) {
          confirm_button_flag = false;
          if (typeof onconfirm === 'function' && onconfirm(product) !== false) {
              box.fadeOut(300, function() {
                confirm_button_flag = true;
                window.history.back();
              });
          } else {
            confirm_button_flag = true;
          }
        }
    });
};

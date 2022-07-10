// ADDING PRODUCTS TO CART
$("#content").on("click", ".add-to-cart", function (event) {
  event.preventDefault();
  let product_id = $(this).data("product-id");
  $.ajax({
    url: "/shop/add-to-cart/",
    data: { product_id: product_id },
    type: "GET",
    success: function (res) {
      $("#cart").html(res);
      $(".cart-quantity").html("(" + $(".total-quantity").html() + ")");
    },
    error: function () {
      alert("Error");
    },
  });
});

// CLEARING THE CART
function clearCart(event) {
  event.preventDefault();
  if (confirm("Are you sure?")) {
    $.ajax({
      url: "/shop/clear-all-fm-cart/",
      type: "GET",
      success: function (res) {
        $("#cart").html(res);
        if ($(".total-quantity").html()) {
          $(".cart-quantity").html("(" + $(".total-quantity").html() + ")");
        } else {
          $(".cart-quantity").html("( )");
        }
      },
      error: function () {
        alert("Error");
      },
    });
  }
}

// OPENING THE CART
function openCart(event) {
  event.preventDefault();
  $.ajax({
    url: "/shop/open-cart/",
    type: "GET",
    success: function (res) {
      $("#cart").html(res);
    },
    error: function () {
      alert("Error");
    },
  });
}

// ACCESSING DYNAMICALLY CREATED BUTTON (.start-buy) VIA PARENT ELEMENT(.modal-body)
$(".modal-body").on("click", ".start-buy", function () {
  $("#cartModal").modal("hide");
});

// DELETING OF ITEMS FROM CART
$(".modal-body").on("click", ".delete", function () {
  let id = $(this).data("id");
  $.ajax({
    url: "/shop/delete-item/",
    data: { id: id },
    type: "GET",
    success: function (res) {
      $("#cart").html(res);
      if ($(".total-quantity").html()) {
        $(".cart-quantity").html("(" + $(".total-quantity").html() + ")");
      } else {
        $(".cart-quantity").html("( )");
      }
    },
    error: function () {
      alert("Error");
    },
  });
});

// FOR GOING TO OPENING ORDER MODAL
$(".modal-content").on("click", ".btn-next", function () {
  $.ajax({
    url: "/shop/create-order/",
    type: "GET",
    success: function (res) {
      $("#order").html(res);
      $("#cartModal").modal("hide");
      $("#orderModal").modal("show");
    },
    error: function () {
      alert("Error");
    },
  });
});

// STYLING OF BUTTON FOR OPENING CART
if ($(window).width() <= 430) {
  $(".btn-cart-modal-open").css("margin", "1rem 0 1rem 0");
}
$(window).resize(function () {
  if ($(window).width() <= 430) {
    $(".btn-cart-modal-open").css("margin", "1rem 1rem 0 0");
  } else {
    $(".btn-cart-modal-open").css("margin", "0 0 0 1rem");
  }
});

// CITY AUTOCOMPLETE NOVAPOSHTA
$("#order").on("input", "#novaposhta_id_city", function () {
  const urlNovaPoshta = "https://api.novaposhta.ua/v2.0/json/";
  let search_val = $(this).val();
  $(this).autocomplete({
    source: function (request, response) {
      $.ajax({
        url: urlNovaPoshta,
        method: "POST",
        timeout: 0,
        headers: {
          "Content-Type": "application/json",
          Accept: "*/*",
        },
        data: JSON.stringify({
          apiKey: "",
          modelName: "Address",
          calledMethod: "searchSettlements",
          methodProperties: {
            CityName: search_val,
            Limit: 5,
          },
        }),
        success: function (res) {
          let city_names = [];
          res["data"][0]["Addresses"].forEach(function (item) {
            city_names.push(item["Present"]);
            response(city_names);
          });
        },
        error: function (error) {
          alert(error);
        },
      });
    },
    minLength: 2,
  });
});

// STREET AUTOCOMPLETE NOVAPOSHTA
$("#order").on("input", "#novaposhta_id_street", function () {
  const urlNovaPoshta = "https://api.novaposhta.ua/v2.0/json/";
  let search_val = $(this).val();
  const city = $("#order").find("#id_city").val();
  const street = $("#order").find("#novaposhta_id_street");
  function getCityRef() {
    if (city) {
      $.ajax({
        url: urlNovaPoshta,
        method: "POST",
        timeout: 0,
        headers: {
          "Content-Type": "application/json",
          Accept: "*/*",
        },
        data: JSON.stringify({
          apiKey: "",
          modelName: "Address",
          calledMethod: "searchSettlements",
          methodProperties: {
            CityName: city,
            Limit: 5,
          },
        }),
        success: function (res) {
          let cityRef = res["data"][0]["Addresses"][0]["Ref"];
          street.autocomplete({
            source: function (request, response) {
              $.ajax({
                url: urlNovaPoshta,
                method: "POST",
                timeout: 0,
                headers: {
                  "Content-Type": "application/json",
                  Accept: "*/*",
                },
                data: JSON.stringify({
                  apiKey: "",
                  modelName: "Address",
                  calledMethod: "searchSettlementStreets",
                  methodProperties: {
                    StreetName: search_val,
                    SettlementRef: cityRef,
                    Limit: 5,
                  },
                }),
                success: function (res) {
                  let street_names = [];
                  res["data"][0]["Addresses"].forEach(function (item) {
                    street_names.push(item["Present"]);
                    response(street_names);
                  });
                },
                error: function (error) {
                  alert(error);
                },
              });
            },
            minLength: 2,
          });
        },
        error: function (error) {
          alert(error);
        },
      });
    } else {
      console.log("No city entered.");
    }
  }
  getCityRef();
});

// POST OFFICE AUTOCOMPLETE NOVAPOSHTA
$("#order").on("input", "#novaposhta_id_post_office", function () {
  const urlNovaPoshta = "https://api.novaposhta.ua/v2.0/json/";
  let search_val = $(this).val();
  const city = $("#order").find("#novaposhta_id_city").val();
  const post_office = $("#order").find("#novaposhta_id_post_office");
  function getPostOffices() {
    if (city) {
      $.ajax({
        url: urlNovaPoshta,
        method: "POST",
        timeout: 0,
        headers: {
          "Content-Type": "application/json",
        },
        data: JSON.stringify({
          apiKey: "",
          modelName: "Address",
          calledMethod: "searchSettlements",
          methodProperties: {
            CityName: city,
            Limit: 5,
          },
        }),
        success: function (res) {
          let cityRef = res["data"][0]["Addresses"][0]["Ref"];
          post_office.autocomplete({
            source: function (request, response) {
              $.ajax({
                url: urlNovaPoshta,
                method: "POST",
                timeout: 0,
                headers: {
                  "Content-Type": "application/json",
                },
                data: JSON.stringify({
                  modelName: "AddressGeneral",
                  calledMethod: "getWarehouses",
                  methodProperties: {
                    SettlementRef: cityRef,
                    FindByString: search_val,
                    Limit: 5,
                  },
                  apiKey: "",
                }),
                success: function (res) {
                  let post_offices = [];
                  res["data"].forEach(function (item) {
                    post_offices.push(item["DescriptionRu"]);
                    response(post_offices);
                  });
                },
                error: function (error) {
                  alert(error);
                },
              });
            },
            minLength: 2,
          });
        },
        error: function (error) {
          alert(error);
        },
      });
    } else {
      alert("No city entered.");
    }
  }
  getPostOffices();
});

// PRODUCT SEARCH AUTOCOMPLETE
$("header").on("input", "#search-site", function () {
  let search_val = $(this).val();
  $(this).autocomplete({
    source: function (request, response) {
      $.ajax({
        url: "/shop/product-search-autocomplete/",
        method: "GET",
        data: { data: search_val },
        success: function (res) {
          let prods = res["data"];
          response(prods);
        },
        error: function (error) {
          alert(error);
        },
      });
    },
    minLength: 2,
  });
});

// SHOWING PRODUCTS IN DIFFERENT CATEGORIES
$(".category-link-item").on("click", function (event) {
  event.preventDefault();
  let category_id = $(this).data("category-id");
  $.ajax({
    url: "/shop/category/" + category_id + "/",
    data: { category_id: category_id },
    type: "GET",
    success: function (res) {
      $("#content").html(res);
    },
    error: function () {
      alert("Error");
    },
  });
});

// SHOWING PRODUCTS OF SEARCH VALUE
$("header").on("click", ".search-products-button", function (event) {
  event.preventDefault();
  let search_val = $("header").find("#search-site").val();
  $.ajax({
    url: "/shop/product-search/",
    data: { data: search_val },
    type: "GET",
    success: function (res) {
      $("#content").html(res);
    },
    error: function () {
      alert("Error");
    },
  });
});

// ADDING PRODUCTS TO CART AND OPENING CART
$("#content").on("click", ".add-to-cart-and-open", function (event) {
  event.preventDefault();
  let product_id = $(this).data("product-id-direct");
  $.ajax({
    url: "/shop/add-to-cart/",
    data: { product_id: product_id },
    type: "GET",
    success: function (res) {
      $("#cart").html(res);
      $(".cart-quantity").html("(" + $(".total-quantity").html() + ")");
      $("#cartModal").modal("show");
    },
    error: function () {
      alert("Error");
    },
  });
});

// CLOSE MODAL ORDER
$("#order").on("click", ".close-modal-order", function () {
  $("#orderModal").modal("hide");
});
// CLOSE MODAL CART
$("#cart").on("click", ".close-modal-cart", function () {
  $("#cartModal").modal("hide");
});

// ADDING PRODUCTS TO CART WITH QUANTITY PLUS BUTTON
$("#cart").on("click", ".quantity-plus", function () {
  let product_id = $(this).data("id");
  $.ajax({
    url: "/shop/add-to-cart/",
    data: { product_id: product_id },
    type: "GET",
    success: function (res) {
      $("#cart").html(res);
      $(".cart-quantity").html("(" + $(".total-quantity").html() + ")");
    },
    error: function () {
      alert("Error");
    },
  });
});

// SUBSTRUCTING FROM ITEMS OF CART WITH QUANTITY MINUS BUTTON
$("#cart").on("click", ".quantity-minus", function () {
  let id = $(this).data("id");
  $.ajax({
    url: "/shop/substruct-fm-item/",
    data: { id: id },
    type: "GET",
    success: function (res) {
      $("#cart").html(res);
      if ($(".total-quantity").html()) {
        $(".cart-quantity").html("(" + $(".total-quantity").html() + ")");
      } else {
        $(".cart-quantity").html("( )");
      }
    },
    error: function () {
      alert("Error");
    },
  });
});

// DELIVERY SHOWING/HIDING
$("#order").on("click", ".form-check-input", function () {
  let del_id = $(this).data("service-id");
  let ser_id = $(this).attr("id");
  $(".delivery-method-details-" + del_id).css("display", "none");
  $(
    ".delivery-method-details-" +
      del_id +
      "[data-delivery-method-id=" +
      ser_id +
      "]"
  ).css("display", "block");
});
// DELIVERY AJAX
$("#order").on("click", ".nav-link", function (e) {
  e.preventDefault();
  $(".nav-link").removeClass("active");
  $(".nav-link").removeAttr("aria-current");
  $(this).addClass("active");
  $(this).attr("aria-current", "page");
  let service_slug = $(this).data("slug");
  $.ajax({
    url: "/shop/choose-delivery/",
    data: { service_slug: service_slug },
    type: "GET",
    success: function (res) {
      $("#choose-delivery").html(res);
    },
    error: function () {
      alert("Error");
    },
  });
});

$("#order").on("click", "#ordered-product-change", function () {
  $("#orderModal").modal("hide");
  $("#cartModal").modal("show");
});

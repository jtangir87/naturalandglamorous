/* Add to Cart */

$(function () {
    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        var quantityCount = $(this).prev().val();
        $.ajax({
            url: btn.attr("data-url"),
            type: "get",
            dataType: "json",
            data: {
                "quantity": quantityCount,
            },
            beforeSend: function () {
                $("#modal-cart .modal-content").html("");
                $("#modal-cart").modal("show");
            },
            success: function (data) {
                $("#modal-cart .modal-content").html(data.html_form);
            },
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: "json",
            success: function (data) {
                if (data.form_is_valid) {
                    console.log("form valid")
                    $("#modal-cart").modal("hide");
                    $("#modal-cart-added").modal("show");
                } else {
                    $("#modal-cart .modal-content").html(data.html_form);
                }
            },
        });
        return false;
    };

    // Add To Cart
    $(".js-add-to-cart").click(loadForm);
    $("#modal-cart").on("submit", ".js-add-to-cart-form", saveForm);
    $(".js-add-to-cart-direct").on("submit", saveForm);
});

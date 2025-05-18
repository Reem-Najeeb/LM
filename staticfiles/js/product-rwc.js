$(document).ready(function () {
    console.log("rwc")
    // Rate call function:-
    //rate();
    rate_conflict();

    // WishList Item  Products
    $(document).on('click', ".add-remove-wishlist", function () {
        var product_id = $(this).attr('data-product');
        var btn = $(this);
        // var wishlistUrl = "{% url 'wishlist_ar' %}";
        var wishlistUrlar = "/ar/product/wishlist_ar";
        console.log(product_id);
        $.ajax({
            // url: '/ar/product/products/wishlist_ar',
            url: wishlistUrlar,
            data: {
                product: product_id
            },
            dataType: 'json',
            success: function (res) {
                console.log("con")
                console.log("cons" + res)

                var addW = btn.find('.add-wishlist');
                var removeW = btn.find('.remove-wishlist');

                if (res.bool) {
                    addW.hide();
                    removeW.show();
                } else {
                    addW.show();
                    removeW.hide();
                }
                updateWishlistCount();
            },
            error: function (xhr) {
                if (xhr.status === 401) {
                    var res = xhr.responseJSON;
                    var message = res.message;
                    var type = res.bool;
                    showAlert(type, message);

                    // alert('يجب تسجيل الدخول أولاً لإضافة المنتج إلى المفضلة');
                } else {
                    var message = 'يجب تسجيل الدخول';
                    var type = 'error';
                    showAlert(type, message);
                    // alert('حدث خطأ ما، الرجاء المحاولة لاحقًا.');
                }
            }
        })
    })



    //  Cart Item  Products
    $(document).on('click', ".add-remove-cartItem", function () {
        var product_id = $(this).attr('data-product');
        var btn = $(this);

        console.log("Adding product:", product_id);
        var url = ""; // تعيين الرابط حسب الشرط

        if (window.location.href.includes("wishlist/")) {
            url = "/ar/product/products/single_cartItem_ar";
        } else {
            url = "/ar/product/single_cartItem_ar";
        }

        $.ajax({
            // url: "single_cartItem_ar",
            url: url,
            data: { product_id: product_id }, // تأكد من أن المفتاح يتطابق مع الـ view
            dataType: 'json',
            success: function (res) {
                console.log(res);
                var addW = btn.find('.add-cart');
                var removeW = btn.find('.remove-cart');
                if (res.bool) {
                    addW.hide();
                    removeW.show();
                } else {
                    addW.show();
                    removeW.hide();
                }
                updateCartItemCount();
            },
            error: function (xhr) {
                if (xhr.status === 401) {
                    var res = xhr.responseJSON;
                    var message = res.message;
                    var type = res.bool;
                    showAlert(type, message);

                    // alert('يجب تسجيل الدخول أولاً لإضافة المنتج إلى المفضلة');
                } else {
                    var message = 'يجب تسجيل الدخول';
                    var type = 'error';
                    showAlert(type, message);
                    // alert('حدث خطأ ما، الرجاء المحاولة لاحقًا.');
                }
            }
        });

    });
    console.log("4")

});

$(document).ready(function () {
    $('.btn-remove1').click(function () {
        var id =  $(this).attr('data-product-id');
        // console.log(id);
        req = $.ajax({
            url : '/delete_cart_product/',
            type: 'POST',
            data:{product_id: id}
        });
        req.done(function () {
            $(this).parents("li").remove();
            // location.reload();
        })
    })
    //     ,
    // $('.add_cart').click(function () {
    //     // console.log(111)
    //     var id = $(this).children().attr('value')
    //     req = $.ajax({
    //         url : '/add_cart/',
    //         type: 'POST',
    //         data:{product_id: id},
    //         success:function () {
    //             // $(this).parents("li").remove();
    //             location.reload();
    //         }
    //     });
    // })
})
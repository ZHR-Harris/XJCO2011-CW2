$(document).ready(function () {
    $('.btn-remove1').click(function () {
        var id =  $(this).attr('data-product-id');
        console.log(id);
        // console.log($(this));
        $.ajax({
            url : '/delete_cart_product/',
            type: 'POST',
            data:{product_id: id},
            success:function (){
                // console.log('kkk')
                $(this).parents("li").remove();
                location.reload();
                // console.log('ppp');
            }
        });
        // req.done(function () {
            // location.reload();
        // })
    });
    $('.qty').blur(function () {
        var num = $(this).val();
        var id = $(this).attr('data-id')
        var single_price = $(this).parents('td').next().children().children().attr('data-price');
        var sub_total = parseInt(num) * parseInt(single_price);
        $(this).parents('td').next().children().children().html("$" + sub_total);
        $.ajax({
            url : '/change_product_num/',
            type: 'POST',
            data:{product_id: id, num: num},
            success:function (data){
                // console.log("success111");
                $("#subtotal").html("$" + data.total_price);
                $("#grandtotal").html("$" + data.total_price);
            }
        });
    });
    // $('button.detail_add').click(function () {
    //     console.log(111)
    //     var id = $(this).children().attr('value')
    //     req = $.ajax({
    //         url : '/addcart/',
    //         type: 'POST',
    //         data:{product_id: id}
    //         // ,
    //         // success:function () {
    //         //     console.log(111);
    //         //     location.reload();
    //         //     console.log(222);
    //         //
    //         // }
    //     });
    //     req.done(function () {
    //         location.reload();
    //     })
    // });
    $('.cart_remove').click(function () {
        var id = $(this).attr('data-id');
        $.ajax({
            url: '/delete_cart_product/',
            type: 'POST',
            data:{product_id: id},
            success:function () {
                $(this).parents('tr').remove();
            }
        })
    });
})

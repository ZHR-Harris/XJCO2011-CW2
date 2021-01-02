$(document).ready(function () {
    $('.btn-remove1').click(function () {
        var id =  $(this).attr('data-product-id');
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
                location.reload();
            }
        });
    });
    $('button.detail_add').click(function () {
        var id = $(this).attr('data-id');
        var num = $(this).prev().children().children('input').val();
        // console.log(num);
        $.ajax({
            url : '/addcart/',
            type: 'POST',
            data:{product_id: id, num: num},
            success:function () {
                // console.log(111);
                location.reload();
                // console.log(222);

            }
        });
    });
    $('.cart_remove').click(function () {
        var id = $(this).attr('data-id');
        $.ajax({
            url: '/delete_cart_product/',
            type: 'POST',
            data:{product_id: id},
            success:function () {
                $(this).parents('tr').remove();
                location.reload();
            }
        })
    });
    $('.delete_address').click(function () {
        var id = $(this).attr('data-address_id');
        $.ajax({
            url: '/delete_address/',
            type: 'POST',
            data:{address_id: id},
            success:function () {
                $(this).parents('tr').remove();
                location.reload();
            }
        })
    });
    $('.s').click(function () {
        if ($(this).attr('id'))
            $(this).removeAttr('id')
        else{
            $(this).siblings().removeAttr('id');
            $(this).attr('id', 'star');
        }
    });
    $('#add_review').click(function () {
        var id = $(this).attr('data-product-id');
        var content = $('#comment').val();
        var rating = $('#star').text();
        $.ajax({
            url: '/add_review/',
            type: 'POST',
            data:{product_id: id, content: content, rating: rating},
            success:function () {
                location.reload();
            }
        })
    });
})

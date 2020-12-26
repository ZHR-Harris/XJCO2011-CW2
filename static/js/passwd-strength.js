//密码的可见与隐藏
// console.log($('#inputPwd'))
var eyeFlag = false;
$('.eye_icon').click(function(){
    if(!eyeFlag){
        $(this).css({'background-image': 'url(' + "../static/images/close_eye.png" + ')'});
        $('#pass1').attr('type','text');
        $('#pass2').attr('type','text');
    }else{
        $(this).css({'background-image': 'url(' + "../static/images/open_eye.png" + ')'});
        $('#pass1').attr('type','password')
        $('#pass2').attr('type','password');
    }
    eyeFlag = !eyeFlag;
})
//密码强度验证
function passValidate(e) {
    var pwd = $.trim(e.value);
    if (pwd === '') {
        $('.pwdStrength').css({'display':'none'})
        $('.weak').css({
            'background': 'rgb(238, 238, 238)'
        });
        $('.middle').css({
            'background': 'rgb(238, 238, 238)'
        });
        $('.strong').css({
            'background': 'rgb(238, 238, 238)'
        });
        $('.result').text('')
    } else {
        $('.pwdStrength').css({'display':'flex'})
        //密码为八位及以上并且字母数字特殊字符三项都包括
        var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
        //密码为七位及以上并且字母、数字、特殊字符三项中有两项，强度是中等
        var mediumRegex = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
        var enoughRegex = new RegExp("(?=.{6,}).*", "g");
        if (false == enoughRegex.test(pwd)) {
        } else if (strongRegex.test(pwd)) {
            $('.strong').css({
                'background': '#33ff33'
            });
            $('.result').text('Strong')
        } else if (mediumRegex.test(pwd)) {

            $('.middle').css({
                'background': '#FFC125'
            });
            $('.strong').css({
                'background': 'rgb(238, 238, 238)'
            });
            $('.result').text('Medium')
        } else {

            $('.weak').css({
                'background': '#EE4000'
            });
            $('.middle').css({
                'background': 'rgb(238, 238, 238)'
            });
            $('.strong').css({
                'background': 'rgb(238, 238, 238)'
            });
            $('.result').text('Low')
        }
    }
}

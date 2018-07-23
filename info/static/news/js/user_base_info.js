function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {

    $(".base_info").submit(function (e) {
        e.preventDefault();

        var signature = $("#signature").val();
        var nick_name = $("#nick_name").val();
        var gender = $(".gender").val();

        if (!nick_name) {
            alert('请输入昵称');
            return
        }
        if (!gender) {
            alert('请选择性别')
        }

        // 修改用户信息接口
        const params = {
            signature,
            nick_name,
            gender
        };

        $.ajax({
            url:"/user/base_info",
            type:"post",
            contentType:"application/json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            data:JSON.stringify(params)
        })
            .done(res =>{
                if (res.errno == 0) {
                    // 更新父窗口内容
                    $('.user_center_name', parent.document).html(params['nick_name']);
                    $('#nick_name', parent.document).html(params['nick_name']);
                    $('.input_sub').blur()
                }else {
                    alert(res.errmsg)
                }
            })
    })
});
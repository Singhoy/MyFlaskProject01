function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {

    $(".focused").click(function () {
        // 取消关注当前新闻作者
        const user_id = $(this).attr('data-userid');
        const params = {
            "action": "unfollow",
            user_id
        };
        $.ajax({
            url: "news/followed_user",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params)
        })
            .done(res => {
                if (res.errno == 0) {
                    // 取消关注成功刷新当前界面
                    window.location.reload()
                } else if (res.errno == 4101) {
                    // 未登录，弹出登录框
                    $('.login_form_con').show()
                } else {
                    // 取消关注失败
                    alert(res.errmsg)
                }
            })

    })
});
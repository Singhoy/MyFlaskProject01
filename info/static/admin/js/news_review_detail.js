function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    $(".news_review").submit(function (e) {
        e.preventDefault();

        // 新闻审核提交
        let params = {};
        // 获取到所有的参数
        $(this).serializeArray().map(x => {
            params[x.name] = x.value
        });
        // 取到参数以便判断
        const action = params["action"];
        const news_id = params["news_id"];
        const reason = params["reason"];
        if (action == "reject" && !reason) {
            alert('请输入拒绝原因');
            return
        }
        params = {
            action,
            news_id,
            reason
        };
        $.ajax({
            url: "/admin/news_review_detail",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params)
        })
            .done(res => {
                if (res.errno == 0) {
                    // 返回上一页,刷新数据
                    location.href = document.referrer
                } else {
                    alert(res.errmsg)
                }
            })
    })
});

// 点击取消，返回上一页
function cancel() {
    history.go(-1)
}
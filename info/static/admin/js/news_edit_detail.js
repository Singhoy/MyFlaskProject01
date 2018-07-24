function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    $(".news_edit").submit(function (e) {
        e.preventDefault();

        // 新闻编辑提交
        $(this).ajaxSubmit({
            beforeSubmit: req => {
                // 在提交之前,对参数进行处理
                for (let i = 0; i < req.length; i++) {
                    let item = req[i];
                    if (item["name"] == "content") {
                        item["value"] = tinyMCE.activeEditor.getContent()
                    }
                }
            },
            url: "/admin/news_edit_detail",
            type: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: res => {
                if (res.errno == 0) {
                    // 返回上一页,刷新数据
                    location.href = document.referrer
                } else {
                    alert(res.errmsg)
                }
            }
        })

    })
});

// 点击取消，返回上一页
function cancel() {
    history.go(-1)
}
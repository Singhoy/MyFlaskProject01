function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {

    // 打开登录框
    $('.comment_form_logout').click(function () {
        $('.login_form_con').show();
    });

    // 收藏
    $(".collection").click(function () {
        const news_id = $(".collection").attr('data_newsid');
        const action = "collect";
        const params = {
            news_id,
            action
        };
        $.ajax({
            url: "/news/news_collect",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params)
        })
            .done(res => {
                if (res.errno == 0) {
                    // 收藏成功
                    // 隐藏收藏按钮
                    $(".collection").hide();
                    // 显示取消收藏按钮
                    $(".collected").show()
                } else if (res.errno == 4101) {
                    $('.login_form_con').show()
                } else {
                    alert(res.errmsg)
                }
            })
    });

    // 取消收藏
    $(".collected").click(function () {
        const news_id = $(".collected").attr('data_newsid');
        const action = "cancel_collect";
        const params = {
            news_id,
            action
        };
        $.ajax({
            url: "/news/news_collect",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params)
        })
            .done(res => {
                if (res.errno == 0) {
                    // 收藏成功
                    // 显示收藏按钮
                    $(".collection").show();
                    // 隐藏取消收藏按钮
                    $(".collected").hide()
                } else if (res.errno == 4101) {
                    $('.login_form_con').show()
                } else {
                    alert(res.errmsg)
                }
            })
    });

    // 评论提交
    $(".comment_form").submit(function (e) {
        e.preventDefault();
        const news_id = $(this).attr('data-newsid');
        const comment = $(".comment_input").val();

        if (!comment) {
            alert('请输入评论内容');
            return
        }
        const params = {
            news_id,
            comment
        };
        $.ajax({
            url: "/news/news_comment",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params)
        })
            .done(res => {
                if (res.errno == 0) {
                    const comment = res.data;
                    // 拼接内容
                    let comment_html = '';
                    comment_html += '<div class="comment_list">';
                    comment_html += '<div class="person_pic fl">';
                    if (comment.user.avatar_url) {
                        comment_html += '<img src="' + comment.user.avatar_url + '" alt="用户图标">'
                    } else {
                        comment_html += '<img src="../../static/news/images/person01.png" alt="用户图标">'
                    }
                    comment_html += '</div>';
                    comment_html += '<div class="user_name fl">' + comment.user.nick_name + '</div>';
                    comment_html += '<div class="comment_text fl">';
                    comment_html += comment.content;
                    comment_html += '</div>';
                    comment_html += '<div class="comment_time fl">' + comment.create_time + '</div>';

                    comment_html += '<a href="javascript:;" class="comment_up fr" data-commentid="' + comment.id + '" data-newsid="' + comment.news_id + '">赞</a>';
                    comment_html += '<a href="javascript:;" class="comment_reply fr">回复</a>';
                    comment_html += '<form class="reply_form fl" data-commentid="' + comment.id + '" data-newsid="' + news_id + '">';
                    comment_html += '<textarea class="reply_input"></textarea>';
                    comment_html += '<input type="button" value="回复" class="reply_sub fr">';
                    comment_html += '<input type="reset" name="" value="取消" class="reply_cancel fr">';
                    comment_html += '</form>';

                    comment_html += '</div>';
                    // 拼接到内容的前面
                    $(".comment_list_con").prepend(comment_html);
                    // 让comment_sub 失去焦点
                    $('.comment_sub').blur();
                    // 清空输入框内容
                    $(".comment_input").val("")
                } else {
                    alert(res.errmsg)
                }
            })

    });

    $('.comment_list_con').delegate('a,input', 'click', function () {

        var sHandler = $(this).prop('class');

        if (sHandler.indexOf('comment_reply') >= 0) {
            $(this).next().toggle();
        }

        if (sHandler.indexOf('reply_cancel') >= 0) {
            $(this).parent().toggle();
        }

        // 点赞
        if (sHandler.indexOf('comment_up') >= 0) {
            const t = $(this);
            let action = "add";
            if (sHandler.indexOf('has_comment_up') >= 0) {
                // 如果当前该评论已经是点赞状态，再次点击会进行到此代码块内，代表要取消点赞
                action = "remove"
            }
            const comment_id = t.attr("data-commentid");
            const news_id = t.attr("data-newsid");
            const params = {
                comment_id,
                action,
                news_id
            };
            $.ajax({
                url: "/news/comment_like",
                type: "post",
                contentType: "application/json",
                headers: {
                    "X-CSRFToken": getCookie("csrf_token")
                },
                data: JSON.stringify(params)
            })
                .done(res => {
                    if (res.errno == 0) {
                        let like_count = t.attr('data-likecount');

                        if (like_count == undefined) {
                            like_count = 0
                        }

                        // 更新点赞按钮图标
                        if (action == "add") {
                            like_count = parseInt(like_count) + 1;
                            // 代表是点赞
                            t.addClass('has_comment_up')
                        } else {
                            like_count = parseInt(like_count) - 1;
                            t.removeClass('has_comment_up')
                        }
                        // 更新点赞数据
                        t.attr('data-likecount', like_count)
                        if (like_count == 0) {
                            t.html("赞")
                        }else {
                            t.html(like_count)
                        }
                    } else if (res.errno == 4101) {
                        $('.login_form_con').show()
                    } else {
                        alert(res.errmsg)
                    }
                })
        }

        // 回复评论
        if (sHandler.indexOf('reply_sub') >= 0) {
            const t = $(this);
            const news_id = t.parent().attr('data-newsid');
            const parent_id = t.parent().attr('data-commentid');
            const comment = t.prev().val();

            if (!comment) {
                alert('请输入评论内容');
                return
            }
            const params = {
                news_id,
                comment,
                parent_id
            };
            $.ajax({
                url: "/news/news_comment",
                type: "post",
                contentType: "application/json",
                headers: {
                    "X-CSRFToken": getCookie("csrf_token")
                },
                data: JSON.stringify(params)
            })
                .done(res => {
                    if (res.errno == 0) {
                        const comment = res.data;
                        // 拼接内容
                        let comment_html = '';
                        comment_html += '<div class="comment_list">';
                        comment_html += '<div class="person_pic fl">';
                        if (comment.user.avatar_url) {
                            comment_html += '<img src="' + comment.user.avatar_url + '" alt="用户图标">'
                        } else {
                            comment_html += '<img src="../../static/news/images/person01.png" alt="用户图标">'
                        }
                        comment_html += '</div>';
                        comment_html += '<div class="user_name fl">' + comment.user.nick_name + '</div>';
                        comment_html += '<div class="comment_text fl">';
                        comment_html += comment.content;
                        comment_html += '</div>';
                        comment_html += '<div class="reply_text_con fl">';
                        comment_html += '<div class="user_name2">' + comment.parent.user.nick_name + '</div>';
                        comment_html += '<div class="reply_text">';
                        comment_html += comment.parent.content;
                        comment_html += '</div>';
                        comment_html += '</div>';
                        comment_html += '<div class="comment_time fl">' + comment.create_time + '</div>';

                        comment_html += '<a href="javascript:;" class="comment_up fr" data-commentid="' + comment.id + '" data-newsid="' + comment.news_id + '">赞</a>';
                        comment_html += '<a href="javascript:;" class="comment_reply fr">回复</a>';
                        comment_html += '<form class="reply_form fl" data-commentid="' + comment.id + '" data-newsid="' + news_id + '">';
                        comment_html += '<textarea class="reply_input"></textarea>';
                        comment_html += '<input type="button" value="回复" class="reply_sub fr">';
                        comment_html += '<input type="reset" name="" value="取消" class="reply_cancel fr">';
                        comment_html += '</form>';

                        comment_html += '</div>';
                        $(".comment_list_con").prepend(comment_html);
                        // 请空输入框
                        t.prev().val('');
                        // 关闭
                        t.parent().hide()
                    } else {
                        alert(res.errmsg)
                    }
                })
        }

        // 更新评论条数
        let updateCommentCount = () => {
            let length = $(".comment_list").length;
            $(".comment_count").html(length + "条评论")
        };

        updateCommentCount()
    });

// 关注当前新闻作者
    $(".focus").click(function () {

    })

// 取消关注当前新闻作者
    $(".focused").click(function () {

    })
})
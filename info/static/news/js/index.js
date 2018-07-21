var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {
    // 首次进入，去加载新闻列表数据
    updateNewsData();
    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid')
        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        $(this).addClass('active')

        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        // 判断页数，去更新新闻数据
        if ((canScrollHeight - nowScroll) < 100) {
            // 将“是否正在向后端查询新闻数据”的标志设置为真
            house_data_querying = true;
            // 如果当前页面数还没达到总页数
            if (cur_page < total_page) {
                // 向后端发送请求，查询下一页新闻数据
                updateNewsData();
            } else {
                house_data_querying = false
            }
        }
    })
});

function updateNewsData() {
    // 更新新闻数据
    const params = {
        "page": 1,
        "cid": currentCid,
        'per_page': 10
    };
    $.get("/news_list", params, res => {
        // 设置“数据正在查询数据”变量为false，以便下次上拉加载
        data_querying = false;
        if (res) {
            // 记录总页数
            total_page = res.totalPage;
            // 如果当前页数为1，则清空原有的数据
            if (cur_page == 1) {
                $(".list_con").html('');
            }
            // 当前页数递增
            cur_page += 1;
            // 显示数据
            for (let i = 0; i < res.newsList.length; i++) {
                let news = res.newsList[i];
                let content = '<li>';
                content += '<a href="#" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>';
                content += '<a href="#" class="news_title fl">' + news.title + '</a>';
                content += '<a href="#" class="news_detail fl">' + news.digest + '</a>';
                content += '<div class="author_info fl">';
                content += '<div class="source fl">来源：' + news.source + '</div>';
                content += '<div class="time fl">' + news.create_time + '</div>';
                content += '</div>';
                content += '</li>';
                $(".list_con").append(content)
            }
        }
    })
}

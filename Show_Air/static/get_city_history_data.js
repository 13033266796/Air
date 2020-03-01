$(function () {
    $('#Map div').click(function (e) {
        var a = $(this).next().text(); // 获取城市
        a = a.split(" ");
        // alert("haha");
        if(a[0].length === 0){
            window.location.replace('/index');
        }
        else {
            window.location.replace('/get_city_history_data/?city='+a[0].split(":")[0]);
        }

        e.stopPropagation();// 阻止事件冒泡
    });

});
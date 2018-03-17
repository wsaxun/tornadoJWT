$(document).ready(function () {
    function getUrlParam(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    }

    get_token = function () {
        top.token = getUrlParam('token')
        return token
    }

    common_init = function () {
        $('.logout a').attr('href', API.logout);
        $('.hardware a').attr('href', API.hardwareView + '?token=' + token)
        $('.hardwaretype a').attr('href', API.hardwareTypeView + '?token=' + token)
        $('.history a').attr('href', API.historyView + '?token=' + token)
        $('.product a').attr('href', API.mainView + '?token=' + token)
        $('.productschema a').attr('href', API.productSchemaView + '?token=' + token)
        $('.price a').attr('href', API.priceView + '?token=' + token)
        $('.output a').attr('href', API.outputView + '?token=' + token)

    }

    operation = function (action, type, data, url, success_callback, error_callback, complete_callback, success_func) {
        $.ajax({
            url: url + '?token=' + token,
            data: JSON.stringify({
                'type': type,
                'action': action,
                'data': data
            }),
            type: 'post',
            dataType: 'json',
            headers: {
                "Accept": "application/json",
                "Content-Type": 'appliaction/json'
            },
            cache: false,
            success: function (data) {
                if (data.ret == 0) {
                    console.log('success')
                    if (success_func == 'None') {
                        console.log('function null')
                    } else {
                        success_func(data)
                    }
                } else if (data.ret >= 0) {
                    alert(data.ret_msg);
                }
                if (success_callback == 'None') {
                    console.log()
                } else {
                    success_callback()
                }
            },
            error: function (data) {
                alert(data.responseJSON.ret_msg)
                if (error_callback == 'None') {
                    console.log()
                } else {
                    error_callback()
                }
            },
            complete: function () {
                if (complete_callback == 'None') {
                    console.log()
                } else {
                    complete_callback()
                }
            }
        });
    }

    check_args_is_null = function () {
        for (var i = 0; i < arguments.length; i++) {
            if (arguments[i] == '' || arguments[i] == undefined || arguments[i] == null) {
                return true
            }
        }
    }
})
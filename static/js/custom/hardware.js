$(document).ready(function () {
// 子应用集显示 & 更新
    display = function () {
        tmp_result = [];
        $('#table').bootstrapTable({
            pagination: true,    //显示分页
            pageNumber: 1,       //首页页码
            pageSize: 10,        //首页分页数量
            pageList: [10, 20, 30, 'All'],   //分页数量
            search: true,           //显示搜索框
            searchText: '',         //默认搜索字符串
            showColumns: true,    //内容下来列表
            showToggle: true,    //切换视图按钮
            method: 'post',      //ajax提交数据方式
            sortName: 'f_id',   //排序字段
            sortOrder: 'desc',  //排序名称
            idField: 'f_id',    //主键
            showRefresh: true,   //显示刷新
            url: API.hardware + '?token=' + token,  //接口
            method: 'post',
            queryParams: function () {       //接口参数
                return {
                    'action': 'query',
                    'type': 'hardware',
                    'data': 'all'
                }
            },
            toolbar: '#toolbar',   //工具栏
            uniqueId: 'f_id',    //唯一键
            columns: [{
                checkbox: 'true'
            }, {
                field: 'index',
                title: '编号',
                formatter: function (value, row, index) {          //格式化
                    return '<span class="badge">' + (index + 1) + '</span>'
                }
            },
                {
                    field: 'f_id',
                    title: 'ID',
                    visible: false,             // 是否可见
                    sortable: true             //是否排序
                }, {
                    field: 'f_name',
                    title: '硬件',
                    editable: {
                        mode: 'popup',
                        validate: function (v) {
                            if (!v) return '不能为空';
                        }
                    }
                }, {
                    field: 'f_type',
                    title: '硬件类型',
                    editable: {
                        type: 'select',
                        source: function () {
                            return tmp_result
                        }
                    }
                }, {
                    field: 'f_description',
                    title: '描述',
                    width: '30%',
                    editable: {
                        mode: 'popup',
                        validate: function (v) {
                            if (!v) return '不能为空';
                        }
                    }
                }
            ],
            onEditableSave: function (field, row, oldValue, $el) {
                action = 'update';
                type = 'hardware';
                data = [{
                    'f_id': row.f_id,
                    'f_name': row.f_name,
                    'f_type': row.f_type,
                    'f_description': row.f_description
                }];
                url = API.hardware;
                complate_callback = 'None';
                error_callback = 'None';
                success_func = 'None';
                success_callback = function () {
                    $('#table').bootstrapTable("refresh");
                };
                operation(action, type, data, url, success_callback, error_callback, complate_callback, success_func);
            },
            onPreBody: function () {
                $.ajax({
                    url: API.hardwaretype + '?token=' + token,
                    type: "post",
                    data: JSON.stringify({
                        'type': 'hardwaretype',
                        'action': 'query',
                        'data': 'all'
                    }),
                    async: false,
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json"
                    },
                    success: function (data) {
                        top.tmp_result = [];
                        for (var i = 1; i <= data.data.length; i++) {
                            tmp_result.push({
                                value: data.data[i - 1].f_id,
                                text: data.data[i - 1].f_name
                            });
                        }
                    }
                });
            }
        })
    }

    $('#add').click(function () {
        action = 'add';
        type = 'hardware';
        if (check_args_is_null($('#modal .name').val(), $('#modal .description').val())) {
            return false
        }
        data = [{
            'f_name': $('#modal .name').val(),
            'f_description': $('#modal .description').val()
        }];
        url = API.hardware;
        complate_callback = function () {
            $('#table').bootstrapTable("refresh");
        };
        error_callback = 'None';
        success_func = 'None';
        success_callback = function () {
            $('#modal').modal('hide');
        };
        operation(action, type, data, url, success_callback, error_callback, complate_callback, success_func);
    })

})
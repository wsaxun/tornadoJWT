$(document).ready(function () {
// 子应用集显示 & 更新
    display = function () {
        $('#table').bootstrapTable({
            pagination: true,
            pageNumber: 1,
            pageSize: 10,
            pageList: [10, 20, 30, 'All'],
            search: true,
            searchText: '',
            showColumns: true,
            showToggle: true,
            method: 'post',
            sortName: 'f_id',
            sortOrder: 'desc',
            idField: 'f_id',
            showRefresh: true,
            searchOnEnterKey: true,
            url: API.product + '?token=' + token,
            queryParams: function () {
                return {
                    'type': 'product',
                    'action': 'query',
                    'data': 'all'
                }
            },
            toolbar: '#toolbar',
            uniqueId: 'f_id',
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
                    visible: false,
                    sortable: true
                }, {
                    field: 'f_name',
                    title: '产品名',
                    sortable: true
                }, {
                    field: 'f_description',
                    title: '描述',
                    width: '30%'
                }
            ],
        })
    }

    $('#add').click(function () {
        action = 'add';
        type = 'product';
        if (check_args_is_null($('#modal .name').val(), $('#modal .description').val())) {
            return false
        }
        data = [{
            'f_name': $('#modal .name').val(),
            'f_description': $('#modal .description').val()
        }];
        url = API.product;
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
$(document).ready(function () {
// 子应用集显示 & 更新
    display = function () {
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
            sortName: 'f_h_id',   //排序字段
            sortOrder: 'desc',  //排序名称
            idField: 'f_id',    //主键
            showRefresh: true,   //显示刷新
            url: API.price + '?token=' + token,  //接口
            method: 'post',
            queryParams: function () {       //接口参数
                return {
                    'action': 'query',
                    'type': 'price',
                    'data': 'all'
                }
            },
            uniqueId: 'f_h_id',    //唯一键
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
                    field: 'f_h_id',
                    title: 'ID',
                    visible: false,             // 是否可见
                    sortable: true             //是否排序
                }, {
                    field: 'f_name',
                    title: '硬件'
                }, {
                    field: 'f_id',
                    title: '价格ID',
                    visible: false,             // 是否可见
                    sortable: true             //是否排序
                }, {
                    field: 'f_business_price',
                    title: '商务价',
                    editable: {
                        mode: 'popup',
                        validate: function (v) {
                            if (!v) return '不能为空';
                        }
                    }
                }, {
                    field: 'f_cost_price',
                    title: '成本价',
                    editable: {
                        mode: 'popup',
                        validate: function (v) {
                            if (!v) return '不能为空';
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
                url = API.price;
                complate_callback = function () {
                        $('#table').bootstrapTable("refresh");
                    };
                error_callback = 'None';
                success_func = 'None';
                success_callback = 'None';
                type = 'price';
                if (row.f_id == null) {
                    action = 'add';
                    if (field == 'f_business_price') {
                        data = [{
                            'f_hardware_id': row.f_h_id,
                            'f_business_price': row.f_business_price,
                        }]
                    }
                    ;
                    if (field == 'f_cost_price') {
                        data = [{
                            'f_hardware_id': row.f_h_id,
                            'f_cost_price': row.f_cost_price,
                        }]
                    }
                    ;
                    if (field == 'f_description') {
                        data = [{
                            'f_hardware_id': row.f_h_id,
                            'f_description': row.f_description,
                        }]
                    }
                    ;
                    operation(action, type, data, url, success_callback, error_callback, complate_callback, success_func);
                } else {
                    action = 'update';
                    data = [{
                        'f_id': row.f_id,
                        'f_business_price': row.f_business_price,
                        'f_cost_price': row.f_cost_price,
                        'f_description': row.f_description
                    }];
                    operation(action, type, data, url, success_callback, error_callback, complate_callback, success_func);

                }
            }
        })
    }
})
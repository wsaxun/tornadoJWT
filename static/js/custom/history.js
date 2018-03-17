$(document).ready(function () {
// 子应用集显示 & 更新
    display = function () {
        $('#table').bootstrapTable({
            pagination: true,
            pageNumber: 1,
            pageSize: 10,
            pageList: [10, 20, 30, 'All'],
            searchText: '',
            showColumns: true,
            showToggle: true,
            method: 'post',
            sortName: 'f_create_time',
            sortOrder: 'desc',
            idField: 'f_id',
            showRefresh: true,
            search: true,
            searchOnEnterKey: true,
            sidePagination: "server",
            url: API.history + '?token=' + token,
            method: 'post',
            uniqueId: 'f_id',
            queryParams: function (params) {
                search = $('.search input').val();
                if (search !== '') {
                    return {
                        'type': 'history',
                        'action': 'query',
                        'offset': params.offset,
                        'limit': params.limit,
                        'search': search,
                        'sort': params.sort,
                        'order': params.order
                    }
                } else {
                    return {
                        'type': 'history',
                        'action': 'query',
                        'offset': params.offset,
                        'limit': params.limit,
                        'sort': params.sort,
                        'order': params.order
                    }
                }
            },
            responseHandler: function (res) {
                return {'total': res.total, 'rows': res.data}
            },
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
                    field: 'f_create_time',
                    title: '时间',
                    sortable: true
                }, {
                    field: 'f_name',
                    title: '产品名',
                    sortable: true
                }, {
                    field: 'f_config',
                    title: '报价单',
                    width: '50%'
                }, {
                    field: 'f_description',
                    title: '描述',
                }
            ]
        })
    }

})
$(document).ready(function() {
    top.API = {
      // 登录api
      login: '/api/user/login',
      // 登出api
      logout: '/api/user/logout',
      // 硬件
      hardware: '/api/device/hardware',
      // 硬件类型
      hardwaretype: '/api/device/hardwaretype',
      // 价格
      price: '/api/device/price',
      // 产品
      product: '/api/device/product',
      // history
      history: '/api/device/history',
      // 主页
      mainView: '/main',
      productSchemaView: '/productschema',
      hardwareView: '/hardware',
      hardwareTypeView: '/hardwaretype',
      historyView: '/history',
      priceView: '/price',
      outputView: '/output'
    }
})
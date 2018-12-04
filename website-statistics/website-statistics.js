// 创建link标签
var link = document.createElement('link');
// 设置rel属性
link.rel = 'stylesheet';
// 设置type属性
link.type = 'text/css';
// 设置media属性
link.media = 'all';
// 数据
var server = 'http://127.0.0.1:5001/', // 记录服务器
    current = encodeURIComponent(window.location.href), // 当前页面地址
    dtss = (new Date()).getTime().toString(); // 当前时间（毫秒）
// 设置href属性
link.href = server + '?url=' + current + '&_vt=' + dtss;
// 获取link容器
var elem = document.querySelector('head') || document.body;
// 将link添加到页面上（link.href指定的资源开始加载）
elem.appendChild(link);
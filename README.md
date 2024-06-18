# flaskx
Flask的加强版，几秒钟让你创建一个项目，加入了一些定制化功能。

## 整体结构
```markdown
├── application                     // 工程名称
│   ├── celery.py                   // celery 默认配置
│   ├── settings.py                 // 项目的settings配置
│   └── urls.py                     // 项目主URL对应关系
├── configs                        // 配置信息
│   ├── config.py                   // 自定义的配置信息
│   └── config-template.json       // 配置文件模版，自行根据config-template.json复制重命名为config.json
├── utils                         // 全局自定义封装工具方法存放位置
│   ├── system                      // flaskx 系统工具
│   └── common                     // 全局公用方法
├── scripts                       // 脚本存放目录
├── logs                          // 日志存放位置
├── apps                          // 应用模块存放目录
├── └── ...
├── media                         // 上传的文件存放位置
├── plugins                       // flaskx 插件目录
├── └── ...
├── middleware                    // flaskx 中间件目录
├── └── ...
├── README.md               // 项目的说明文档
├── LICENSE                 // 开源 LICENSE
├── app.py                  // 项目启动入口
└── requirements.txt        // 项目环境依赖
```

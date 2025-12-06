# 任务分发工具

一个轻量级的任务分发与追踪工具，支持任务创建、流转、留言、实时通知等功能。

## 项目结构

```
taskManager/
├── docs/                    # 设计文档
│   ├── 整体架构设计.md
│   ├── 数据库设计.md
│   ├── backend/            # 后端模块设计文档
│   ├── frontend/           # 前端设计文档
│   └── client/             # 客户端设计文档
├── backend/                # 后端代码 (Flask + Python)
├── frontend/               # 前端代码 (Vue.js)
├── client/                 # 客户端代码
│   └── chrome-extension/   # Chrome插件
└── 任务分发工具.md          # 产品需求文档
```

## 技术栈

### 后端
- **Flask 2.3+**: Web框架
- **SQLite3**: 数据库（开发环境，生产环境推荐PostgreSQL）
- **SQLAlchemy**: ORM
- **Flask-SocketIO**: WebSocket支持
- **APScheduler**: 定时任务

### 前端
- **Vue 3**: 前端框架
- **Element Plus**: UI组件库
- **Vite**: 构建工具
- **Socket.IO Client**: WebSocket客户端

### 客户端
- **Chrome Extension**: 浏览器插件

## 快速开始

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量文件（可选，使用默认配置即可）
cp .env.example .env

# 初始化数据库（自动创建SQLite数据库文件）
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 创建管理员账户
python init_db.py

# 启动服务
python run.py
```

后端服务将运行在 `http://localhost:5000`

**注意**: SQLite数据库文件 `taskmanager.db` 会自动创建在 `backend` 目录下。

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 复制环境变量文件
cp .env.example .env

# 启动开发服务器
npm run dev
```

前端服务将运行在 `http://localhost:5173`

### 3. Chrome插件安装

1. 打开Chrome浏览器
2. 访问 `chrome://extensions/`
3. 启用"开发者模式"
4. 点击"加载已解压的扩展程序"
5. 选择 `client/chrome-extension` 文件夹
6. 点击插件图标，配置服务器地址和用户UM编号

## 默认账户

- 邮箱: `admin@example.com`
- 密码: `admin123`

**注意**: 使用 `python init_db.py` 命令可以创建默认管理员账户。

## 创建管理员账户

项目已包含初始化脚本 `backend/init_db.py`，运行即可创建默认管理员：

```bash
cd backend
python init_db.py
```

默认管理员信息：
- UM编号: `UM001`
- 姓名: `系统管理员`
- 邮箱: `admin@example.com`
- 密码: `admin123`

**重要**: 首次登录后请立即修改密码！

## 开发说明

### 后端开发

- **添加新的API接口**: 在 `backend/app/api/` 下创建新的蓝图
- **添加新的模型**: 在 `backend/app/models/` 下创建模型文件
- **添加业务逻辑**: 在 `backend/app/services/` 下创建服务类

### 前端开发

- **添加新页面**: 在 `frontend/src/views/` 下创建Vue组件
- **添加新组件**: 在 `frontend/src/components/` 下创建组件
- **添加API**: 在 `frontend/src/api/` 下添加API函数

## 生产部署

**注意**: 生产环境建议使用PostgreSQL数据库以获得更好的性能和并发支持。

### 数据库迁移到PostgreSQL（生产环境推荐）

```bash
# 1. 安装PostgreSQL
# 2. 创建数据库
createdb taskmanager

# 3. 安装PostgreSQL驱动
pip install psycopg2-binary

# 4. 修改.env文件
DATABASE_URL=postgresql://user:password@localhost:5432/taskmanager

# 5. 重新运行迁移
flask db upgrade
python init_db.py
```

### 后端部署

```bash
# 使用Gunicorn + Eventlet
pip install gunicorn eventlet

# 启动
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 run:app
```

### 前端部署

```bash
# 构建
npm run build

# 将 dist 目录部署到Nginx
```

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/taskmanager/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket代理
    location /socket.io {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 常见问题

### Q: 数据库文件在哪里？
A: 开发环境使用SQLite3，数据库文件位于 `backend/taskmanager.db`。

### Q: 如何切换到PostgreSQL？
A: 修改 `.env` 文件中的 `DATABASE_URL`，安装 `psycopg2-binary`，然后重新运行 `flask db upgrade`。

### Q: WebSocket连接失败？
A: 确保后端服务正常运行，检查CORS配置和防火墙设置。

### Q: Chrome插件无法接收通知？
A: 检查插件配置中的服务器地址是否正确，确保服务器可访问。

### Q: 如何重置数据库？
A: 删除 `backend/taskmanager.db` 文件和 `backend/migrations` 目录，然后重新运行初始化命令。

## 文档

详细的设计文档请查看 `docs/` 目录：

- [整体架构设计](docs/整体架构设计.md)
- [数据库设计](docs/数据库设计.md)
- [后端模块设计](docs/backend/)
- [前端架构设计](docs/frontend/前端架构设计.md)
- [Chrome插件设计](docs/client/Chrome插件设计.md)

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

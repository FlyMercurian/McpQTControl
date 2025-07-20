#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , m_mcpServer(nullptr)
    , m_isLoggedIn(false)
    , m_testButtonClickCount(0)
{
    ui->setupUi(this);
    setWindowTitle("MCP Qt Control Application");
    
    // 初始化MCP服务器
    initializeMcpServer();
    
    // 初始状态栏
    updateStatusBar("应用已启动，MCP服务器正在启动...");
}

MainWindow::~MainWindow()
{
    if (m_mcpServer) {
        m_mcpServer->stopServer();
        delete m_mcpServer;
    }
    delete ui;
}

/**
 * 函数名称：`initializeMcpServer`
 * 功能描述：初始化MCP服务器
 * 参数说明：无
 * 返回值：void类型
 */
void MainWindow::initializeMcpServer()
{
    m_mcpServer = new McpServer(this, this);
    
    // 连接MCP服务器信号
    connect(m_mcpServer, &McpServer::serverStarted, this, &MainWindow::onMcpServerStarted);
    connect(m_mcpServer, &McpServer::serverStopped, this, &MainWindow::onMcpServerStopped);
    connect(m_mcpServer, &McpServer::clientConnected, this, &MainWindow::onMcpClientConnected);
    connect(m_mcpServer, &McpServer::clientDisconnected, this, &MainWindow::onMcpClientDisconnected);
    connect(m_mcpServer, &McpServer::commandExecuted, this, &MainWindow::onMcpCommandExecuted);
    
    // 启动服务器
    if (!m_mcpServer->startServer(8088)) {
        QMessageBox::warning(this, "错误", "MCP服务器启动失败！");
    }
}

/**
 * 函数名称：`performLogin`
 * 功能描述：执行登录操作（供MCP调用，和手动点击行为完全一致）
 * 参数说明：
 *     - account：QString类型，账号
 *     - password：QString类型，密码
 * 返回值：bool类型，登录成功状态
 */
bool MainWindow::performLogin(const QString& account, const QString& password)
{
    // 设置输入框内容
    ui->lineEdit_account->setText(account);
    ui->lineEdit_password->setText(password);
    
    // 模拟登录逻辑（这里可以添加实际的登录验证）
    if (account.isEmpty() || password.isEmpty()) {
        QMessageBox::warning(this, "失败", "账号或密码不能为空！");
        return false;
    }
    
    // 简单的演示登录逻辑
    if (account.length() >= 3 && password.length() >= 3) {
        m_isLoggedIn = true;
        m_currentAccount = account;
        m_loginTime = QDateTime::currentDateTime();
        
        // 更新UI状态
        ui->pushButton_login->setText("退出登录");
        ui->lineEdit_account->setEnabled(false);
        ui->lineEdit_password->setEnabled(false);
        
        updateStatusBar(QString("用户 %1 登录成功").arg(account));
        qDebug() << "MCP登录成功:" << account;
        
        // 和手动点击一样显示弹窗
        QMessageBox::information(this, "成功", "登录成功！");
        return true;
    }
    
    // 和手动点击一样显示弹窗
    QMessageBox::warning(this, "失败", "登录失败，请检查账号密码！");
    return false;
}

/**
 * 函数名称：`performTestButton`
 * 功能描述：执行测试按钮点击操作（供MCP调用，和手动点击行为完全一致）
 * 参数说明：无
 * 返回值：bool类型，执行成功状态
 */
bool MainWindow::performTestButton()
{
    bool success = executeTestButtonAction();
    
    if (success) {
        // 和手动点击一样显示弹窗
        QMessageBox::information(this, "测试", QString("测试按钮被点击 %1 次").arg(m_testButtonClickCount));
    }
    
    return success;
}

/**
 * 函数名称：`updateStatusBar`
 * 功能描述：更新状态栏信息
 * 参数说明：
 *     - message：QString类型，状态信息
 * 返回值：void类型
 */
void MainWindow::updateStatusBar(const QString& message)
{
    statusBar()->showMessage(message);
}

/**
 * 函数名称：`resetLoginFields`
 * 功能描述：重置登录输入框
 * 参数说明：无
 * 返回值：void类型
 */
void MainWindow::resetLoginFields()
{
    ui->lineEdit_account->clear();
    ui->lineEdit_password->clear();
    ui->lineEdit_account->setEnabled(true);
    ui->lineEdit_password->setEnabled(true);
    ui->pushButton_login->setText("登录");
}

/**
 * 函数名称：`executeTestButtonAction`
 * 功能描述：执行测试按钮的实际逻辑（避免递归调用）
 * 参数说明：无
 * 返回值：bool类型，执行成功状态
 */
bool MainWindow::executeTestButtonAction()
{
    try {
        m_testButtonClickCount++;
        
        QString message = QString("测试按钮被点击，计数: %1").arg(m_testButtonClickCount);
        updateStatusBar(message);
        qDebug() << "MCP测试按钮点击:" << message;
        
        return true;
    }
    catch (...) {
        qDebug() << "测试按钮执行异常";
        return false;
    }
}

// UI按钮点击事件
void MainWindow::on_pushButton_login_clicked()
{
    if (m_isLoggedIn) {
        // 退出登录
        m_isLoggedIn = false;
        m_currentAccount.clear();
        resetLoginFields();
        updateStatusBar("用户已退出登录");
    } else {
        // 执行登录
        QString account = ui->lineEdit_account->text();
        QString password = ui->lineEdit_password->text();
        
        performLogin(account, password);
    }
}

void MainWindow::on_pushButton_test_clicked()
{
    performTestButton();
}

// MCP服务器事件处理
void MainWindow::onMcpServerStarted(quint16 port)
{
    updateStatusBar(QString("MCP服务器已启动，监听端口: %1").arg(port));
    qDebug() << "MCP服务器启动成功，端口:" << port;
}

void MainWindow::onMcpServerStopped()
{
    updateStatusBar("MCP服务器已停止");
    qDebug() << "MCP服务器已停止";
}

void MainWindow::onMcpClientConnected(const QString& address)
{
    updateStatusBar(QString("MCP客户端连接: %1").arg(address));
    qDebug() << "MCP客户端连接:" << address;
}

void MainWindow::onMcpClientDisconnected(const QString& address)
{
    updateStatusBar(QString("MCP客户端断开: %1").arg(address));
    qDebug() << "MCP客户端断开:" << address;
}

void MainWindow::onMcpCommandExecuted(const QString& command, bool success)
{
    QString status = success ? "成功" : "失败";
    updateStatusBar(QString("MCP命令执行%1: %2").arg(status).arg(command));
    qDebug() << "MCP命令执行:" << command << "结果:" << status;
}


#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QDateTime>
#include "mcpserver.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    /**
     * 函数名称：`performLogin`
     * 功能描述：执行登录操作（供MCP调用）
     * 参数说明：
     *     - account：QString类型，账号
     *     - password：QString类型，密码
     * 返回值：bool类型，登录成功状态
     */
    bool performLogin(const QString& account, const QString& password);

    /**
     * 函数名称：`performTestButton`
     * 功能描述：执行测试按钮点击操作（供MCP调用）
     * 参数说明：无
     * 返回值：bool类型，执行成功状态
     */
    bool performTestButton();

    /**
     * 函数名称：`isLoggedIn`
     * 功能描述：检查登录状态
     * 参数说明：无
     * 返回值：bool类型，登录状态
     */
    bool isLoggedIn() const { return m_isLoggedIn; }

    /**
     * 函数名称：`getCurrentAccount`
     * 功能描述：获取当前登录账号
     * 参数说明：无
     * 返回值：QString类型，当前账号
     */
    QString getCurrentAccount() const { return m_currentAccount; }

private slots:
    void on_pushButton_login_clicked();
    void on_pushButton_test_clicked();
    
    // MCP服务器相关槽函数
    void onMcpServerStarted(quint16 port);
    void onMcpServerStopped();
    void onMcpClientConnected(const QString& address);
    void onMcpClientDisconnected(const QString& address);
    void onMcpCommandExecuted(const QString& command, bool success);

private:
    Ui::MainWindow *ui;
    McpServer *m_mcpServer;
    
    // 状态变量
    bool m_isLoggedIn;
    QString m_currentAccount;
    QDateTime m_loginTime;
    int m_testButtonClickCount;

    /**
     * 函数名称：`initializeMcpServer`
     * 功能描述：初始化MCP服务器
     * 参数说明：无
     * 返回值：void类型
     */
    void initializeMcpServer();

    /**
     * 函数名称：`updateStatusBar`
     * 功能描述：更新状态栏信息
     * 参数说明：
     *     - message：QString类型，状态信息
     * 返回值：void类型
     */
    void updateStatusBar(const QString& message);

    /**
     * 函数名称：`resetLoginFields`
     * 功能描述：重置登录输入框
     * 参数说明：无
     * 返回值：void类型
     */
    void resetLoginFields();

    /**
     * 函数名称：`executeTestButtonAction`
     * 功能描述：执行测试按钮的实际逻辑（避免递归调用）
     * 参数说明：无
     * 返回值：bool类型，执行成功状态
     */
    bool executeTestButtonAction();
};

#endif // MAINWINDOW_H

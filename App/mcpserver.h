#ifndef MCPSERVER_H
#define MCPSERVER_H

#include <QObject>
#include <QTcpServer>
#include <QTcpSocket>
#include <QList>
#include "mcpprocessor.h"
#include "mcpexecutor.h"

class MainWindow;

/**
 * 函数名称：`McpServer`
 * 功能描述：MCP TCP服务器类，处理客户端连接和命令执行
 * 参数说明：无
 * 返回值：无
 */
class McpServer : public QObject
{
    Q_OBJECT

public:
    explicit McpServer(MainWindow* mainWindow, QObject *parent = nullptr);
    ~McpServer();

    /**
     * 函数名称：`startServer`
     * 功能描述：启动TCP服务器
     * 参数说明：
     *     - port：quint16类型，监听端口号
     * 返回值：bool类型，启动成功状态
     */
    bool startServer(quint16 port = 8080);

    /**
     * 函数名称：`stopServer`
     * 功能描述：停止TCP服务器
     * 参数说明：无
     * 返回值：void类型
     */
    void stopServer();

    /**
     * 函数名称：`isRunning`
     * 功能描述：检查服务器运行状态
     * 参数说明：无
     * 返回值：bool类型，运行状态
     */
    bool isRunning() const;

    /**
     * 函数名称：`getPort`
     * 功能描述：获取服务器监听端口
     * 参数说明：无
     * 返回值：quint16类型，端口号
     */
    quint16 getPort() const;

    /**
     * 函数名称：`getConnectedClients`
     * 功能描述：获取连接的客户端数量
     * 参数说明：无
     * 返回值：int类型，客户端数量
     */
    int getConnectedClients() const;

signals:
    /**
     * 函数名称：`serverStarted`
     * 功能描述：服务器启动信号
     * 参数说明：
     *     - port：quint16类型，监听端口号
     * 返回值：void类型
     */
    void serverStarted(quint16 port);

    /**
     * 函数名称：`serverStopped`
     * 功能描述：服务器停止信号
     * 参数说明：无
     * 返回值：void类型
     */
    void serverStopped();

    /**
     * 函数名称：`clientConnected`
     * 功能描述：客户端连接信号
     * 参数说明：
     *     - address：QString类型，客户端地址
     * 返回值：void类型
     */
    void clientConnected(const QString& address);

    /**
     * 函数名称：`clientDisconnected`
     * 功能描述：客户端断开连接信号
     * 参数说明：
     *     - address：QString类型，客户端地址
     * 返回值：void类型
     */
    void clientDisconnected(const QString& address);

    /**
     * 函数名称：`commandExecuted`
     * 功能描述：命令执行完成信号
     * 参数说明：
     *     - command：QString类型，执行的命令
     *     - success：bool类型，执行成功状态
     * 返回值：void类型
     */
    void commandExecuted(const QString& command, bool success);

private slots:
    void onNewConnection();
    void onClientDisconnected();
    void onDataReceived();

private:
    QTcpServer* m_tcpServer;
    QList<QTcpSocket*> m_clients;
    McpProcessor* m_processor;
    McpExecutor* m_executor;
    MainWindow* m_mainWindow;

    /**
     * 函数名称：`processMessage`
     * 功能描述：处理收到的消息
     * 参数说明：
     *     - socket：QTcpSocket*类型，客户端socket
     *     - message：QString类型，消息内容
     * 返回值：void类型
     */
    void processMessage(QTcpSocket* socket, const QString& message);

    /**
     * 函数名称：`sendResponse`
     * 功能描述：发送响应消息给客户端
     * 参数说明：
     *     - socket：QTcpSocket*类型，客户端socket
     *     - response：QString类型，响应内容
     * 返回值：void类型
     */
    void sendResponse(QTcpSocket* socket, const QString& response);

    /**
     * 函数名称：`removeClient`
     * 功能描述：移除客户端连接
     * 参数说明：
     *     - socket：QTcpSocket*类型，客户端socket
     * 返回值：void类型
     */
    void removeClient(QTcpSocket* socket);
};

#endif // MCPSERVER_H 
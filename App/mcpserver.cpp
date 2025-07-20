#include "mcpserver.h"
#include "mainwindow.h"
#include <QDebug>
#include <QHostAddress>
#include <QDateTime>

McpServer::McpServer(MainWindow* mainWindow, QObject *parent)
    : QObject(parent)
    , m_tcpServer(new QTcpServer(this))
    , m_processor(new McpProcessor())
    , m_executor(new McpExecutor(mainWindow))
    , m_mainWindow(mainWindow)
{
    connect(m_tcpServer, &QTcpServer::newConnection, this, &McpServer::onNewConnection);
}

McpServer::~McpServer()
{
    stopServer();
    delete m_processor;
    delete m_executor;
}

/**
 * 函数名称：`startServer`
 * 功能描述：启动TCP服务器
 * 参数说明：
 *     - port：quint16类型，监听端口号
 * 返回值：bool类型，启动成功状态
 */
bool McpServer::startServer(quint16 port)
{
    if (m_tcpServer->isListening()) {
        qDebug() << "服务器已在运行";
        return true;
    }

    if (!m_tcpServer->listen(QHostAddress::Any, port)) {
        qDebug() << "启动服务器失败:" << m_tcpServer->errorString();
        return false;
    }

    qDebug() << "MCP服务器已启动，监听端口:" << m_tcpServer->serverPort();
    emit serverStarted(m_tcpServer->serverPort());
    return true;
}

/**
 * 函数名称：`stopServer`
 * 功能描述：停止TCP服务器
 * 参数说明：无
 * 返回值：void类型
 */
void McpServer::stopServer()
{
    if (!m_tcpServer->isListening()) {
        return;
    }

    // 断开所有客户端连接
    for (QTcpSocket* client : m_clients) {
        client->close();
        client->deleteLater();
    }
    m_clients.clear();

    m_tcpServer->close();
    qDebug() << "MCP服务器已停止";
    emit serverStopped();
}

/**
 * 函数名称：`isRunning`
 * 功能描述：检查服务器运行状态
 * 参数说明：无
 * 返回值：bool类型，运行状态
 */
bool McpServer::isRunning() const
{
    return m_tcpServer->isListening();
}

/**
 * 函数名称：`getPort`
 * 功能描述：获取服务器监听端口
 * 参数说明：无
 * 返回值：quint16类型，端口号
 */
quint16 McpServer::getPort() const
{
    return m_tcpServer->serverPort();
}

/**
 * 函数名称：`getConnectedClients`
 * 功能描述：获取连接的客户端数量
 * 参数说明：无
 * 返回值：int类型，客户端数量
 */
int McpServer::getConnectedClients() const
{
    return m_clients.size();
}

void McpServer::onNewConnection()
{
    while (m_tcpServer->hasPendingConnections()) {
        QTcpSocket* client = m_tcpServer->nextPendingConnection();
        
        connect(client, &QTcpSocket::disconnected, this, &McpServer::onClientDisconnected);
        connect(client, &QTcpSocket::readyRead, this, &McpServer::onDataReceived);
        
        m_clients.append(client);
        
        QString clientAddress = QString("%1:%2")
                               .arg(client->peerAddress().toString())
                               .arg(client->peerPort());
        
        qDebug() << "客户端连接:" << clientAddress;
        emit clientConnected(clientAddress);
    }
}

void McpServer::onClientDisconnected()
{
    QTcpSocket* client = qobject_cast<QTcpSocket*>(sender());
    if (client) {
        QString clientAddress = QString("%1:%2")
                               .arg(client->peerAddress().toString())
                               .arg(client->peerPort());
        
        qDebug() << "客户端断开连接:" << clientAddress;
        emit clientDisconnected(clientAddress);
        
        removeClient(client);
    }
}

void McpServer::onDataReceived()
{
    QTcpSocket* client = qobject_cast<QTcpSocket*>(sender());
    if (!client) return;
    
    while (client->canReadLine()) {
        QByteArray data = client->readLine();
        QString message = QString::fromUtf8(data).trimmed();
        
        if (!message.isEmpty()) {
            qDebug() << "收到消息:" << message;
            processMessage(client, message);
        }
    }
}

/**
 * 函数名称：`processMessage`
 * 功能描述：处理收到的消息
 * 参数说明：
 *     - socket：QTcpSocket*类型，客户端socket
 *     - message：QString类型，消息内容
 * 返回值：void类型
 */
void McpServer::processMessage(QTcpSocket* socket, const QString& message)
{
    // 解析命令
    McpProcessor::ParsedCommand cmd;
    
    // 尝试解析为JSON格式
    if (message.startsWith("{")) {
        cmd = m_processor->parseJsonMessage(message);
    } else {
        // 解析为纯文本命令
        cmd = m_processor->parseCommand(message);
        if (cmd.requestId.isEmpty()) {
            cmd.requestId = QString::number(QDateTime::currentMSecsSinceEpoch());
        }
    }
    
    QString response;
    bool success = false;
    
    // 执行命令
    switch (cmd.type) {
        case McpProcessor::LOGIN: {
            if (cmd.params.size() >= 2) {
                McpExecutor::ExecutionResult result = m_executor->executeLogin(cmd.params[0], cmd.params[1]);
                response = m_processor->formatResponse(cmd.requestId, result.success, result.message, result.data);
                success = result.success;
            } else {
                response = m_processor->formatResponse(cmd.requestId, false, "登录参数不足");
            }
            break;
        }
        case McpProcessor::TEST_BUTTON: {
            McpExecutor::ExecutionResult result = m_executor->executeTestButton();
            response = m_processor->formatResponse(cmd.requestId, result.success, result.message, result.data);
            success = result.success;
            break;
        }
        case McpProcessor::GET_STATE: {
            McpExecutor::ExecutionResult result = m_executor->getState();
            response = m_processor->formatResponse(cmd.requestId, result.success, result.message, result.data);
            success = result.success;
            break;
        }
        default: {
            response = m_processor->formatResponse(cmd.requestId, false, "未知命令: " + cmd.originalMessage);
            break;
        }
    }
    
    // 发送响应
    sendResponse(socket, response);
    emit commandExecuted(cmd.originalMessage, success);
}

/**
 * 函数名称：`sendResponse`
 * 功能描述：发送响应消息给客户端
 * 参数说明：
 *     - socket：QTcpSocket*类型，客户端socket
 *     - response：QString类型，响应内容
 * 返回值：void类型
 */
void McpServer::sendResponse(QTcpSocket* socket, const QString& response)
{
    if (socket && socket->state() == QAbstractSocket::ConnectedState) {
        socket->write(response.toUtf8() + "\n");
        socket->flush();
        qDebug() << "发送响应:" << response;
    }
}

/**
 * 函数名称：`removeClient`
 * 功能描述：移除客户端连接
 * 参数说明：
 *     - socket：QTcpSocket*类型，客户端socket
 * 返回值：void类型
 */
void McpServer::removeClient(QTcpSocket* socket)
{
    if (socket) {
        m_clients.removeAll(socket);
        socket->deleteLater();
    }
} 
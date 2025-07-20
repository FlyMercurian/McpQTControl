#ifndef MCPPROCESSOR_H
#define MCPPROCESSOR_H

#include <QString>
#include <QStringList>
#include <QJsonDocument>
#include <QJsonObject>

/**
 * 函数名称：`McpProcessor`
 * 功能描述：MCP命令解析和处理器类
 * 参数说明：无
 * 返回值：无
 */
class McpProcessor
{
public:
    enum CommandType {
        UNKNOWN = 0,
        LOGIN,          // login:account:password
        TEST_BUTTON,    // testbutton
        GET_STATE       // getstate
    };

    struct ParsedCommand {
        CommandType type;
        QStringList params;
        QString originalMessage;
        QString requestId;
        
        ParsedCommand() : type(UNKNOWN) {}
    };

    McpProcessor();

    /**
     * 函数名称：`parseJsonMessage`
     * 功能描述：解析JSON-RPC格式的MCP消息
     * 参数说明：
     *     - jsonMessage：QString类型，JSON格式的消息字符串
     * 返回值：ParsedCommand类型，解析后的命令结构
     */
    ParsedCommand parseJsonMessage(const QString& jsonMessage);

    /**
     * 函数名称：`parseCommand`
     * 功能描述：解析纯文本命令
     * 参数说明：
     *     - command：QString类型，命令字符串
     * 返回值：ParsedCommand类型，解析后的命令结构
     */
    ParsedCommand parseCommand(const QString& command);

    /**
     * 函数名称：`formatResponse`
     * 功能描述：格式化响应消息为JSON-RPC格式
     * 参数说明：
     *     - requestId：QString类型，请求ID
     *     - success：bool类型，执行成功状态
     *     - message：QString类型，响应消息
     *     - data：QJsonObject类型，附加数据
     * 返回值：QString类型，JSON格式的响应字符串
     */
    QString formatResponse(const QString& requestId, bool success, 
                          const QString& message, const QJsonObject& data = QJsonObject());

private:
    CommandType stringToCommandType(const QString& commandStr);
};

#endif // MCPPROCESSOR_H 
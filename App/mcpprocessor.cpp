#include "mcpprocessor.h"
#include <QDebug>

McpProcessor::McpProcessor()
{
}

/**
 * 函数名称：`parseJsonMessage`
 * 功能描述：解析JSON-RPC格式的MCP消息
 * 参数说明：
 *     - jsonMessage：QString类型，JSON格式的消息字符串
 * 返回值：ParsedCommand类型，解析后的命令结构
 */
McpProcessor::ParsedCommand McpProcessor::parseJsonMessage(const QString& jsonMessage)
{
    ParsedCommand result;
    result.originalMessage = jsonMessage;
    
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(jsonMessage.toUtf8(), &error);
    
    if (error.error != QJsonParseError::NoError) {
        qDebug() << "JSON解析错误:" << error.errorString();
        return result;
    }
    
    QJsonObject obj = doc.object();
    
    // 提取请求ID
    if (obj.contains("id")) {
        result.requestId = obj["id"].toString();
    }
    
    // 提取方法和参数
    if (obj.contains("method") && obj["method"].toString() == "execute") {
        QJsonObject params = obj["params"].toObject();
        if (params.contains("command")) {
            QString command = params["command"].toString();
            ParsedCommand cmdResult = parseCommand(command);
            result.type = cmdResult.type;
            result.params = cmdResult.params;
        }
    }
    
    return result;
}

/**
 * 函数名称：`parseCommand`
 * 功能描述：解析纯文本命令
 * 参数说明：
 *     - command：QString类型，命令字符串
 * 返回值：ParsedCommand类型，解析后的命令结构
 */
McpProcessor::ParsedCommand McpProcessor::parseCommand(const QString& command)
{
    ParsedCommand result;
    result.originalMessage = command;
    
    if (command.startsWith("login:")) {
        result.type = LOGIN;
        QStringList parts = command.split(":");
        if (parts.size() >= 3) {
            result.params << parts[1] << parts[2]; // account, password
        }
    }
    else if (command == "testbutton") {
        result.type = TEST_BUTTON;
    }
    else if (command == "getstate") {
        result.type = GET_STATE;
    }
    else {
        result.type = UNKNOWN;
        qDebug() << "未知命令:" << command;
    }
    
    return result;
}

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
QString McpProcessor::formatResponse(const QString& requestId, bool success, 
                                   const QString& message, const QJsonObject& data)
{
    QJsonObject response;
    response["id"] = requestId;
    
    QJsonObject result;
    result["success"] = success;
    result["message"] = message;
    if (!data.isEmpty()) {
        result["data"] = data;
    }
    
    if (success) {
        response["result"] = result;
    } else {
        QJsonObject error;
        error["code"] = -1;
        error["message"] = message;
        error["data"] = data;
        response["error"] = error;
    }
    
    QJsonDocument doc(response);
    return doc.toJson(QJsonDocument::Compact);
}

/**
 * 函数名称：`stringToCommandType`
 * 功能描述：将字符串转换为命令类型枚举
 * 参数说明：
 *     - commandStr：QString类型，命令字符串
 * 返回值：CommandType类型，对应的命令类型枚举
 */
McpProcessor::CommandType McpProcessor::stringToCommandType(const QString& commandStr)
{
    if (commandStr.startsWith("login:")) {
        return LOGIN;
    } else if (commandStr == "testbutton") {
        return TEST_BUTTON;
    } else if (commandStr == "getstate") {
        return GET_STATE;
    }
    return UNKNOWN;
} 
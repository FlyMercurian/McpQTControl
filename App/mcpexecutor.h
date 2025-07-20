#ifndef MCPEXECUTOR_H
#define MCPEXECUTOR_H

#include <QString>
#include <QJsonObject>

class MainWindow;

/**
 * 函数名称：`McpExecutor`
 * 功能描述：MCP功能执行器类，负责执行具体的UI操作
 * 参数说明：无
 * 返回值：无
 */
class McpExecutor
{
public:
    struct ExecutionResult {
        bool success;
        QString message;
        QJsonObject data;
        
        ExecutionResult(bool s = false, const QString& m = "") 
            : success(s), message(m) {}
    };

    McpExecutor(MainWindow* window);

    /**
     * 函数名称：`executeLogin`
     * 功能描述：执行登录操作
     * 参数说明：
     *     - account：QString类型，账号
     *     - password：QString类型，密码
     * 返回值：ExecutionResult类型，执行结果
     */
    ExecutionResult executeLogin(const QString& account, const QString& password);

    /**
     * 函数名称：`executeTestButton`
     * 功能描述：执行测试按钮点击操作
     * 参数说明：无
     * 返回值：ExecutionResult类型，执行结果
     */
    ExecutionResult executeTestButton();

    /**
     * 函数名称：`getState`
     * 功能描述：获取当前应用状态
     * 参数说明：无
     * 返回值：ExecutionResult类型，包含状态信息的执行结果
     */
    ExecutionResult getState();

private:
    MainWindow* m_mainWindow;

    /**
     * 函数名称：`isValidCredentials`
     * 功能描述：验证登录凭据格式
     * 参数说明：
     *     - account：QString类型，账号
     *     - password：QString类型，密码
     * 返回值：bool类型，验证结果
     */
    bool isValidCredentials(const QString& account, const QString& password);
};

#endif // MCPEXECUTOR_H 
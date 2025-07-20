#include "mcpexecutor.h"
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <QTimer>
#include <QApplication>
#include <QDateTime>

McpExecutor::McpExecutor(MainWindow* window) : m_mainWindow(window)
{
}

/**
 * 函数名称：`executeLogin`
 * 功能描述：执行登录操作
 * 参数说明：
 *     - account：QString类型，账号
 *     - password：QString类型，密码
 * 返回值：ExecutionResult类型，执行结果
 */
McpExecutor::ExecutionResult McpExecutor::executeLogin(const QString& account, const QString& password)
{
    if (!m_mainWindow) {
        return ExecutionResult(false, "主窗口指针为空");
    }
    
    if (!isValidCredentials(account, password)) {
        return ExecutionResult(false, "账号或密码格式无效");
    }
    
    try {
        // 调用主窗口的登录功能
        bool result = m_mainWindow->performLogin(account, password);
        
        if (result) {
            QJsonObject data;
            data["account"] = account;
            data["loginTime"] = QDateTime::currentDateTime().toString();
            
            ExecutionResult execResult(true, "登录成功");
            execResult.data = data;
            return execResult;
        } else {
            return ExecutionResult(false, "登录失败");
        }
    }
    catch (const std::exception& e) {
        qDebug() << "登录执行异常:" << e.what();
        return ExecutionResult(false, QString("登录执行异常: %1").arg(e.what()));
    }
}

/**
 * 函数名称：`executeTestButton`
 * 功能描述：执行测试按钮点击操作
 * 参数说明：无
 * 返回值：ExecutionResult类型，执行结果
 */
McpExecutor::ExecutionResult McpExecutor::executeTestButton()
{
    if (!m_mainWindow) {
        return ExecutionResult(false, "主窗口指针为空");
    }
    
    try {
        // 调用主窗口的测试按钮功能
        bool result = m_mainWindow->performTestButton();
        
        if (result) {
            QJsonObject data;
            data["buttonClicked"] = true;
            data["clickTime"] = QDateTime::currentDateTime().toString();
            
            ExecutionResult execResult(true, "测试按钮执行成功");
            execResult.data = data;
            return execResult;
        } else {
            return ExecutionResult(false, "测试按钮执行失败");
        }
    }
    catch (const std::exception& e) {
        qDebug() << "测试按钮执行异常:" << e.what();
        return ExecutionResult(false, QString("测试按钮执行异常: %1").arg(e.what()));
    }
}

/**
 * 函数名称：`getState`
 * 功能描述：获取当前应用状态
 * 参数说明：无
 * 返回值：ExecutionResult类型，包含状态信息的执行结果
 */
McpExecutor::ExecutionResult McpExecutor::getState()
{
    if (!m_mainWindow) {
        return ExecutionResult(false, "主窗口指针为空");
    }
    
    try {
        QJsonObject state;
        state["windowTitle"] = m_mainWindow->windowTitle();
        state["isVisible"] = m_mainWindow->isVisible();
        state["isEnabled"] = m_mainWindow->isEnabled();
        state["currentTime"] = QDateTime::currentDateTime().toString();
        state["applicationVersion"] = QApplication::applicationVersion();
        
        // 获取登录状态（如果主窗口有相关方法）
        // state["isLoggedIn"] = m_mainWindow->isLoggedIn();
        
        ExecutionResult result(true, "状态获取成功");
        result.data = state;
        return result;
    }
    catch (const std::exception& e) {
        qDebug() << "状态获取异常:" << e.what();
        return ExecutionResult(false, QString("状态获取异常: %1").arg(e.what()));
    }
}

/**
 * 函数名称：`isValidCredentials`
 * 功能描述：验证登录凭据格式
 * 参数说明：
 *     - account：QString类型，账号
 *     - password：QString类型，密码
 * 返回值：bool类型，验证结果
 */
bool McpExecutor::isValidCredentials(const QString& account, const QString& password)
{
    // 基本格式验证
    if (account.isEmpty() || password.isEmpty()) {
        return false;
    }
    
    // 账号长度限制
    if (account.length() < 3 || account.length() > 50) {
        return false;
    }
    
    // 密码长度限制
    if (password.length() < 3 || password.length() > 100) {
        return false;
    }
    
    return true;
} 
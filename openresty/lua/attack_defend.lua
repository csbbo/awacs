local checker = require "libinjection"

local detecte_content = {
    uri = ngx.var.uri,
    request_body = ngx.unescape_uri(ngx.var.request_body),
    http_referer = ngx.var.http_referer,
    http_user_agent = ngx.var.http_user_agent
}

for k, v in pairs(detecte_content) do
    local issqli_attack, finger = checker.sqli(v)
    local isxss_attack = checker.xss(v)
    if issqli_attack or isxss_attack then
        if issqli_attack then
            ngx.log(ngx.ALERT, "SQL injection attack detected: ", v)
        else
            ngx.log(ngx.ALERT, "XSS attack detected: ", v)
        end
        
        ngx.exec("/attack_defend")
    end
end
#!/usr/bin/env bash

set -u

HOST="${1:-127.0.0.1}"
PORT="${2:-8080}"
URL="${3:-http://${HOST}:${PORT}/health}"

REPORT="connectivity_report_$(date +%Y%m%d_%H%M%S).txt"
BODY_FILE="$(mktemp)"
ERR_FILE="$(mktemp)"

trap 'rm -f "$BODY_FILE" "$ERR_FILE"' EXIT

{
    echo "========== 推理服务连通性报告 =========="
    echo "时间: $(date '+%F %T')"
    echo "目标主机: $HOST"
    echo "目标端口: $PORT"
    echo "探测 URL: $URL"
    echo

    echo "[1] ss 端口监听检查"

    if ! command -v ss >/dev/null 2>&1; then
        echo "结果: 未找到 ss 命令"
    else
        ALL_LISTEN="$(ss -tlnp 2>/dev/null || true)"
        LISTEN_INFO="$(
            printf '%s\n' "$ALL_LISTEN" |
            awk -v pattern=":${PORT}$" 'NR > 1 && $4 ~ pattern'
        )"

        if [[ -n "$LISTEN_INFO" ]]; then
            echo "结果: 端口正在监听"
            echo "$LISTEN_INFO"
        else
            echo "结果: 未发现端口监听"
        fi
    fi

    echo
    echo "[2] curl HTTP 连通性检查"

    if ! command -v curl >/dev/null 2>&1; then
        echo "结果: 未找到 curl 命令"
    else
        HTTP_CODE="$(
            curl -sS \
                 -o "$BODY_FILE" \
                 -w '%{http_code}' \
                 --connect-timeout 3 \
                 --max-time 8 \
                 "$URL" 2>"$ERR_FILE"
        )"
        CURL_RC=$?

        [[ -n "$HTTP_CODE" ]] || HTTP_CODE="000"

        echo "curl 返回码: $CURL_RC"
        echo "HTTP 状态码: $HTTP_CODE"

        if (( CURL_RC == 0 )); then
            case "$HTTP_CODE" in
                2*)
                    echo "结果: HTTP 服务正常"
                    ;;
                3*)
                    echo "结果: 服务可访问，但发生重定向"
                    ;;
                4*)
                    echo "结果: 网络可达，但请求或接口可能有问题"
                    ;;
                5*)
                    echo "结果: 服务端内部错误"
                    ;;
                *)
                    echo "结果: 已连接，但 HTTP 状态异常"
                    ;;
            esac
        else
            echo "结果: HTTP 连接失败"
            if [[ -s "$ERR_FILE" ]]; then
                echo "错误信息:"
                sed 's/^/  /' "$ERR_FILE"
            fi
        fi
    fi

    echo
    echo "========== 报告结束 =========="
} | tee "$REPORT"

echo
echo "报告已保存到: $REPORT"

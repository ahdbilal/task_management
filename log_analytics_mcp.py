#!/usr/bin/env python3
"""
Log Analytics MCP Server
Provides tools for Claude to query and analyze application logs
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
from typing import List, Dict, Any

# MCP imports
from mcp.server import Server
from mcp.types import Tool, TextContent

# Log directory
LOGS_DIR = Path("/home/azureuser/staging/logs") if Path("/home/azureuser/staging").exists() else Path("./logs")

app = Server("log-analytics")

def read_log_file(filename: str, max_lines: int = 1000) -> List[Dict]:
    """Read and parse JSON log file"""
    log_file = LOGS_DIR / filename
    if not log_file.exists():
        return []
    
    logs = []
    with open(log_file, 'r') as f:
        for line in f.readlines()[-max_lines:]:  # Get last N lines
            try:
                logs.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return logs

def filter_logs(logs: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
    """Filter logs based on criteria"""
    filtered = logs
    
    if "level" in filters:
        filtered = [log for log in filtered if log.get("level") == filters["level"]]
    
    if "module" in filters:
        filtered = [log for log in filtered if log.get("module") == filters["module"]]
    
    if "endpoint" in filters:
        filtered = [log for log in filtered if filters["endpoint"] in log.get("endpoint", "")]
    
    if "min_duration_ms" in filters:
        filtered = [log for log in filtered if log.get("duration_ms", 0) >= filters["min_duration_ms"]]
    
    if "since_minutes" in filters:
        cutoff = datetime.utcnow() - timedelta(minutes=filters["since_minutes"])
        filtered = [log for log in filtered if datetime.fromisoformat(log.get("timestamp", "")) > cutoff]
    
    return filtered

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available log analytics tools"""
    return [
        Tool(
            name="query_logs",
            description="Query application logs with filters. Returns recent log entries matching criteria.",
            inputSchema={
                "type": "object",
                "properties": {
                    "log_type": {
                        "type": "string",
                        "enum": ["app", "errors"],
                        "description": "Type of logs to query: 'app' for all logs, 'errors' for errors only"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        "description": "Filter by log level"
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "Filter by endpoint path (partial match)"
                    },
                    "module": {
                        "type": "string",
                        "description": "Filter by module name"
                    },
                    "min_duration_ms": {
                        "type": "number",
                        "description": "Filter requests slower than this (in milliseconds)"
                    },
                    "since_minutes": {
                        "type": "number",
                        "description": "Only show logs from the last N minutes"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of log entries to return",
                        "default": 50
                    }
                },
                "required": ["log_type"]
            }
        ),
        Tool(
            name="analyze_errors",
            description="Analyze error logs and provide summary statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "since_minutes": {
                        "type": "number",
                        "description": "Analyze errors from the last N minutes",
                        "default": 60
                    }
                }
            }
        ),
        Tool(
            name="get_slow_requests",
            description="Find slow API requests above a duration threshold",
            inputSchema={
                "type": "object",
                "properties": {
                    "threshold_ms": {
                        "type": "number",
                        "description": "Duration threshold in milliseconds",
                        "default": 1000
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results",
                        "default": 20
                    }
                }
            }
        ),
        Tool(
            name="get_endpoint_stats",
            description="Get statistics for API endpoints (request count, avg duration, error rate)",
            inputSchema={
                "type": "object",
                "properties": {
                    "since_minutes": {
                        "type": "number",
                        "description": "Analyze from the last N minutes",
                        "default": 60
                    }
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "query_logs":
        log_type = arguments["log_type"]
        filename = "errors.log" if log_type == "errors" else "app.log"
        limit = arguments.get("limit", 50)
        
        logs = read_log_file(filename, max_lines=1000)
        
        # Apply filters
        filters = {k: v for k, v in arguments.items() if k not in ["log_type", "limit"]}
        if filters:
            logs = filter_logs(logs, filters)
        
        logs = logs[-limit:]  # Take last N entries
        
        result = f"Found {len(logs)} log entries:\n\n"
        for log in logs:
            result += f"[{log.get('timestamp', 'N/A')}] {log.get('level', 'INFO')}: {log.get('message', '')}\n"
            if log.get('endpoint'):
                result += f"  Endpoint: {log['endpoint']}\n"
            if log.get('duration_ms'):
                result += f"  Duration: {log['duration_ms']}ms\n"
            if log.get('exception'):
                result += f"  Exception: {log['exception'][:200]}...\n"
            result += "\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "analyze_errors":
        since_minutes = arguments.get("since_minutes", 60)
        
        logs = read_log_file("errors.log", max_lines=1000)
        logs = filter_logs(logs, {"since_minutes": since_minutes})
        
        if not logs:
            return [TextContent(type="text", text="No errors found in the specified time range.")]
        
        # Count by module
        modules = Counter(log.get("module", "unknown") for log in logs)
        # Count by endpoint
        endpoints = Counter(log.get("endpoint", "N/A") for log in logs)
        
        result = f"📊 Error Analysis (last {since_minutes} minutes)\n\n"
        result += f"Total Errors: {len(logs)}\n\n"
        
        result += "Top Modules with Errors:\n"
        for module, count in modules.most_common(5):
            result += f"  • {module}: {count} errors\n"
        
        result += "\nTop Endpoints with Errors:\n"
        for endpoint, count in endpoints.most_common(5):
            result += f"  • {endpoint}: {count} errors\n"
        
        result += "\nRecent Error Messages:\n"
        for log in logs[-5:]:
            result += f"  • [{log.get('timestamp', 'N/A')}] {log.get('message', '')}\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_slow_requests":
        threshold_ms = arguments.get("threshold_ms", 1000)
        limit = arguments.get("limit", 20)
        
        logs = read_log_file("app.log", max_lines=1000)
        
        # Filter for slow requests
        slow_logs = [log for log in logs if log.get("duration_ms", 0) >= threshold_ms]
        slow_logs = sorted(slow_logs, key=lambda x: x.get("duration_ms", 0), reverse=True)[:limit]
        
        if not slow_logs:
            return [TextContent(type="text", text=f"No requests slower than {threshold_ms}ms found.")]
        
        result = f"🐌 Slow Requests (>{threshold_ms}ms):\n\n"
        for log in slow_logs:
            result += f"• {log.get('endpoint', 'N/A')} - {log.get('duration_ms', 0)}ms\n"
            result += f"  Time: {log.get('timestamp', 'N/A')}\n"
            result += f"  Method: {log.get('method', 'N/A')}\n\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_endpoint_stats":
        since_minutes = arguments.get("since_minutes", 60)
        
        logs = read_log_file("app.log", max_lines=2000)
        logs = filter_logs(logs, {"since_minutes": since_minutes})
        
        # Group by endpoint
        endpoint_data = {}
        for log in logs:
            endpoint = log.get("endpoint", "unknown")
            if endpoint not in endpoint_data:
                endpoint_data[endpoint] = {
                    "count": 0,
                    "total_duration": 0,
                    "errors": 0,
                    "durations": []
                }
            
            endpoint_data[endpoint]["count"] += 1
            
            if "duration_ms" in log:
                duration = log["duration_ms"]
                endpoint_data[endpoint]["total_duration"] += duration
                endpoint_data[endpoint]["durations"].append(duration)
            
            if log.get("level") in ["ERROR", "CRITICAL"]:
                endpoint_data[endpoint]["errors"] += 1
        
        result = f"📈 Endpoint Statistics (last {since_minutes} minutes):\n\n"
        
        # Sort by request count
        sorted_endpoints = sorted(endpoint_data.items(), key=lambda x: x[1]["count"], reverse=True)
        
        for endpoint, data in sorted_endpoints[:10]:
            avg_duration = data["total_duration"] / data["count"] if data["count"] > 0 else 0
            error_rate = (data["errors"] / data["count"] * 100) if data["count"] > 0 else 0
            
            result += f"• {endpoint}\n"
            result += f"  Requests: {data['count']}\n"
            if data["durations"]:
                result += f"  Avg Duration: {avg_duration:.2f}ms\n"
                result += f"  Max Duration: {max(data['durations']):.2f}ms\n"
            result += f"  Error Rate: {error_rate:.1f}%\n\n"
        
        return [TextContent(type="text", text=result)]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

